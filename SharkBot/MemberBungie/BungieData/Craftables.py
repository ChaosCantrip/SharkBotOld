from dataclasses import dataclass
from typing import Union
import discord

from .BungieData import BungieData
import SharkBot

_CRAFTING_RECORDS: dict[str, dict[str, dict[str, str]]] = {}

to_ignore = ["3091520691", "3091520690", "3091520689", "1388873285"]
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
            if record_hash in to_ignore:
                continue
            record_definition = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(record_hash)
            _CRAFTING_RECORDS[parent_node_name][weapon_type_name][record_hash] = record_definition["displayProperties"]["name"]


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
    def _process_data(data) -> _DATA_TYPE:
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
    def _format_embed_data(embed: discord.Embed, data: _DATA_TYPE, **kwargs):
        output_text = []
        for weapon_type, weapon_subtype_data in data.items():
            output_text.append(f"\n**__{weapon_type}__**\n")
            _data: dict[str, list[str]] = {}
            for weapon_subtype, subtype_data in weapon_subtype_data.items():
                _sub_data = []
                for response in subtype_data:
                    if not response.complete:
                        _sub_data.append(f"- {response.weapon_name} `{response.progress}/{response.quota}`")
                if len(_sub_data) > 0:
                    _data[weapon_subtype] = _sub_data
            if len(data) > 0:
                for weapon_subtype, subtype_data in _data.items():
                    output_text.append(f"**{weapon_subtype}**")
                    output_text.extend(subtype_data)
                    output_text.append("")
            else:
                output_text.extend(f"You have already completed all of your **{weapon_type}**\n")
        embed.description = "\n".join(output_text)