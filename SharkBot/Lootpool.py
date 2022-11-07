import random
from typing import Union, TypedDict

import SharkBot


class Lootpool:
    lootpools = []

    def __init__(self, lootpool_id: str, table: dict[str, str]):
        self.id = lootpool_id
        self._raw_nodes = list(table.keys())
        self._weightings = list(float(weight) for weight in table.values())
        self._built_nodes = None

    @classmethod
    def get(cls, lootpool_id: str) -> Self:
        for lootpool in cls.lootpools:
            if lootpool.id == lootpool_id:
                return lootpool
        else:
            raise SharkBot.Errors.LootpoolNotFoundError(lootpool_id)
