import random
from typing import Union, TypedDict, Self
import json

import SharkBot


class _LootpoolData(TypedDict):
    lootpool_id: str
    table: dict[str, str]


class Lootpool:
    lootpools = []

    def __init__(self, lootpool_id: str, table: dict[str, str]):
        self.id = lootpool_id
        self._nodes = list(table.keys())
        self._weightings = list(float(weight) for weight in table.values())

    def roll(self):
        result = random.choices(self._nodes, weights=self._weightings, k=1)[0]
        result_type, result_target = result.split(":")
        if result_type == "item":
            return SharkBot.Item.get(result_target)
        elif result_type == "collection":
            return random.choice(SharkBot.Collection.get(result_target).items)
        elif result_type == "lootpool":
            return SharkBot.Lootpool.get(result_target).roll()
        else:
            raise SharkBot.Errors.UnknownLootpoolNodeType(self.id, result)

    @classmethod
    def get(cls, lootpool_id: str) -> Self:
        for lootpool in cls.lootpools:
            if lootpool.id == lootpool_id:
                return lootpool
        else:
            raise SharkBot.Errors.LootpoolNotFoundError(lootpool_id)


for filename in SharkBot.Utils.get_dir_filepaths("data/static/collectibles/lootpools", ".json"):
    with open(filename, "r") as infile:
        file_data: list[_LootpoolData] = json.load(infile)
    for lootpool_data in file_data:
        Lootpool.lootpools.append(Lootpool(**lootpool_data))
