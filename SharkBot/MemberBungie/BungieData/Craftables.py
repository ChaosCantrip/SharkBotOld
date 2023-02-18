from typing import Union

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

    @staticmethod
    def _process_data(data):
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