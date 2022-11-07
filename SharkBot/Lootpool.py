import random
from typing import Union, TypedDict

import SharkBot


class Lootpool:
    lootpools = []

    def __init__(self):
        pass

    @classmethod
    def get(cls, lootpool_id: str) -> Self:
        for lootpool in cls.lootpools:
            if lootpool.id == lootpool_id:
                return lootpool
        else:
            raise SharkBot.Errors.LootpoolNotFoundError(lootpool_id)
