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
        self._raw_nodes = list(table.keys())
        self._weightings = list(float(weight) for weight in table.values())
        self._built_nodes = None

    def build(self) -> None:
        self._built_nodes = []
        for raw_node in self._raw_nodes:
            node_type, node_value = raw_node.split(":")
            if node_type == "lootpool":
                self._built_nodes.append(self.get(node_value))
            elif node_type == "collection":
                self._built_nodes.append(SharkBot.Collection.get(node_value))
            elif node_type == "item":
                if node_value == "EVENTBOX":
                    self._built_nodes.append(SharkBot.Item.currentEventBox)
                else:
                    self._built_nodes.append(SharkBot.Item.get(node_value))
            else:
                raise SharkBot.Errors.UnknownLootpoolNodeType(self, raw_node)

    def roll(self):
        if self._built_nodes is None:
            self.build()

        result = random.choices(self._built_nodes, weights=self._weightings, k=1)
        if type(result) == Lootpool:
            return result.roll()
        elif type(result) == SharkBot.Collection.Collection:
            return random.choice(result.items)
        else:
            return result

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
