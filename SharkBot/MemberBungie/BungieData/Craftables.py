import json
from dataclasses import dataclass
from typing import Union, Optional
import discord

from .BungieData import BungieData
from ..ProfileResponseData import ProfileResponseData
import SharkBot

_CRAFTING_RECORDS: dict[str, dict[str, dict[str, str]]] = {}

_CRAFTABLE_WEAPON_NAMES: dict[str, str] = {}

needed_nodes = [127506319, 3289524180, 1464475380]
for node_hash in needed_nodes:
    parent_node_definition: dict = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(node_hash)
    parent_node_name = parent_node_definition["displayProperties"]["name"]
    _CRAFTING_RECORDS[parent_node_name] = {}
    weapon_type_nodes: list[dict] = [SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"]) for d in parent_node_definition["children"]["presentationNodes"]]
    for weapon_type_node in weapon_type_nodes:
        weapon_type_name = weapon_type_node["displayProperties"]["name"]
        _CRAFTING_RECORDS[parent_node_name][weapon_type_name] = {}
        for record_set in weapon_type_node["children"]["records"]:
            record_hash = str(record_set["recordHash"])
            record_definition = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(record_hash)
            weapon_name = record_definition["displayProperties"]["name"]
            if weapon_name == "Classified":
                continue
            _CRAFTING_RECORDS[parent_node_name][weapon_type_name][record_hash] = weapon_name
            _CRAFTABLE_WEAPON_NAMES[weapon_name] = weapon_type_name[:-1]

with open("data/static/bungie/definitions/PatternSources.json", "r") as f:
    _PATTERN_SOURCES: dict[str, list[str | None]] = {
        weapon_name: [weapon_source.lower() for weapon_source in sources] for weapon_name, sources in json.load(f).items()
    }

for _sources in _PATTERN_SOURCES.values():
    _sources.append(None)


@dataclass
class _CraftablesResponse:
    weapon_name: str
    progress: int
    quota: int
    complete: bool


_DATA_TYPE = dict[str, dict[str, list[_CraftablesResponse]]]


class Craftables(BungieData):
    _COMPONENTS = [900]
    _EMBED_TITLE = "Missing Weapon Patterns"
    _THUMBNAIL_URL = "https://www.bungie.net/common/destiny2_content/icons/e7e6d522d375dfa6dec055135ce6a77e.png"

    @staticmethod
    def _process_data(data: ProfileResponseData) -> _DATA_TYPE:
        records = data["profileRecords"]["data"]["records"]
        output: dict[str, dict[str, list[_CraftablesResponse]]] = {}
        for weapon_type, weapon_subtypes_data in _CRAFTING_RECORDS.items():
            output[weapon_type] = {}
            for weapon_subtype, weapons_data in weapon_subtypes_data.items():
                output[weapon_type][weapon_subtype] = []
                for weapon_hash, weapon_name in weapons_data.items():
                    record: dict[str, int | bool] = records[weapon_hash]["objectives"][0]
                    output[weapon_type][weapon_subtype].append(
                        _CraftablesResponse(
                            weapon_name=weapon_name,
                            progress=record["progress"],
                            quota=record["completionValue"],
                            complete=record["complete"]
                        )
                    )
        return output

    @staticmethod
    def _process_cache_write(data: _DATA_TYPE):
        return {
            weapon_type: {
                weapon_subtype: [
                    response.__dict__ for response in weapon_subtype_data
                ] for weapon_subtype, weapon_subtype_data in weapon_type_data.items()
            } for weapon_type, weapon_type_data in data.items()
        }

    @staticmethod
    def _process_cache_load(data: dict[str, dict[str, list[dict[str, str | int | bool]]]]):
        return {
            weapon_type: {
                weapon_subtype: [
                    _CraftablesResponse(**response) for response in weapon_subtype_data
                ] for weapon_subtype, weapon_subtype_data in weapon_type_data.items()
            } for weapon_type, weapon_type_data in data.items()
        }

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data: _DATA_TYPE, source: Optional[str] = None, **kwargs):
        total_patterns = 0
        total_rbs = 0
        output_text = []
        for weapon_type, weapon_subtype_data in data.items():
            weapon_patterns = 0
            weapon_rbs = 0
            _data: dict[str, list[str]] = {}
            for weapon_subtype, subtype_data in weapon_subtype_data.items():
                _sub_data = []
                for response in subtype_data:
                    if source is not None and source.lower() not in _PATTERN_SOURCES[response.weapon_name]:
                        continue
                    if not response.complete:
                        weapon_patterns += 1
                        weapon_rbs += response.quota - response.progress
                        _sub_data.append(f"- {response.weapon_name} `{response.progress}/{response.quota}`")
                if len(_sub_data) > 0:
                    _data[weapon_subtype] = _sub_data
            output_text.append(f"\n**__{weapon_type}__**")
            output_text.append(f"*Patterns Missing:* `{weapon_patterns}`")
            output_text.append(f"*Red Borders Needed:* `{weapon_rbs}`")
            if sum(len(_sub_data) for _sub_data in _data) > 0:
                for weapon_subtype, subtype_data in _data.items():
                    output_text.extend(subtype_data)
            else:
                output_text.append(f"You have already completed all of your **{weapon_type}**\n")
            total_patterns += weapon_patterns
            total_rbs += weapon_rbs
        if source is not None:
            output_text = [f"Source: **__{source}__**"] + output_text
        output_text.append(f"\n**Total Patterns Missing:** `{total_patterns}`")
        output_text.append(f"**Total Red Borders Needed:** `{total_rbs}`")
        embed.description = "\n".join(output_text)

    @staticmethod
    def get_patterns_without_sources() -> list[tuple[str, str]]:
        output = []
        for _weapon_name, _weapon_type in _CRAFTABLE_WEAPON_NAMES.items():
            if _weapon_name not in _PATTERN_SOURCES:
                output.append((_weapon_name, _weapon_type))
        return output
