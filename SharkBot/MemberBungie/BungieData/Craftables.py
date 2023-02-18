from typing import Union
import discord

from .BungieData import BungieData
import SharkBot

_CRAFTING_RECORDS = SharkBot.Utils.JSON.load("data/static/bungie/definitions/CraftingRecords.json")

class _CraftablesResponse:

    def __init__(self, weapon_name: str, sources: list[str], record_data: dict[str, Union[int, bool]]):
        self.weapon_name = weapon_name
        self.sources = sources
        self.progress: int = record_data["progress"]
        self.quota: int = record_data["completionValue"]
        self.complete: bool = record_data["complete"]

    def is_from(self, source: str) -> bool:
        return source in self.sources

    def is_from_any(self, sources: list[str]) -> bool:
        return any([source in self.sources for source in sources])

    @property
    def data(self) -> dict:
        return {
            "weapon_name": self.weapon_name,
            "sources": self.sources,
            "record_data": {
                "progress": self.progress,
                "completionValue": self.quota,
                "complete": self.complete
            }
        }

class Craftables(BungieData):
    _COMPONENTS = [900]
    _EMBED_TITLE = "Missing Weapon Patterns"
    _THUMBNAIL_URL = "https://www.bungie.net/common/destiny2_content/icons/e7e6d522d375dfa6dec055135ce6a77e.png"

    @staticmethod
    def _process_data(data) -> dict[str, list[_CraftablesResponse]]:
        records = data["profileRecords"]["data"]["records"]
        output = {}
        for weapon_type, weapon_records in _CRAFTING_RECORDS.items():
            weapon_data = []
            for weapon in weapon_records:
                weapon_data.append(
                    _CraftablesResponse(
                        weapon_name=weapon["name"],
                        sources=weapon["sources"],
                        record_data=records[weapon["record_hash"]]["objectives"][0]
                    )
                )
            output[weapon_type] = weapon_data
        return output

    @staticmethod
    def _process_cache_write(data):
        return {weapon_type: [response.data for response in responses] for weapon_type, responses in data.items()}

    @staticmethod
    def _process_cache_load(data):
        return {weapon_type: [_CraftablesResponse(**craftable_data) for craftable_data in type_data] for weapon_type, type_data in data.items()}

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data: dict[str, list[_CraftablesResponse]], _sources: list[str] = None, **kwargs):
        output = {}
        for weapon_type, responses in data.items():
            _data = []
            for response in responses:
                if not response.is_from_any(_sources):
                    continue
                if not response.complete:
                    _data.append(f"{SharkBot.Icon.get('source_' + str(response.sources[0]))} **{response.weapon_name}** - {response.progress}/{response.quota}")
            output[weapon_type] = _data
        for weapon_type, _data in output.items():
            if len(_data) == 0:
                embed.add_field(
                    name=f"__{weapon_type}__",
                    value=f"You have finished all your **{weapon_type}**!",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"__{weapon_type}__",
                    value="\n".join(_data),
                    inline=False
                )

        num_left = sum(len([r for r in l if not r.complete]) for l in data.values())
        embed.description = f"You have `{num_left}` patterns left to discover."