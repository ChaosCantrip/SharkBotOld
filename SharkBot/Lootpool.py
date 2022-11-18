import random
from typing import Union, TypedDict
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
        self._possible_items: Union[list, None] = None

    def __repr__(self):
        output = f"Lootpool({self.id})\n"
        output += "\n".join(f"\t-{repr(item)}" for item in self.possible_items())

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

    def possible_items(self) -> list:
        if self._possible_items is not None:
            return self._possible_items

        item_list = []
        for node in self._nodes:
            node_type, node_target = node.split(":")
            if node_type == "item":
                item_list.append(SharkBot.Item.get(node_type))
            elif node_type == "collection":
                item_list = item_list + list(SharkBot.Collection.get(node_target).items)
            elif node_type == "lootpool":
                item_list = item_list + SharkBot.Lootpool.get(node_target).possible_items()
            else:
                raise SharkBot.Errors.UnknownLootpoolNodeType(self.id, node)

        output = []
        for item in item_list:
            if item not in output:
                output.append(item)

        self._possible_items = output
        return output

    @classmethod
    def get(cls, lootpool_id: str):
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
