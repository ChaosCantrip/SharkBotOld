from SharkBot import Collection
import random


class LootPool:

    def __init__(self, loot_pool_code):
        loot_pool_codes = loot_pool_code.split(";")
        self.lootPool = {}
        for code in loot_pool_codes:
            split_code = code.split(":")
            collection = Collection.get(split_code[0])
            chance = int(split_code[1])
            self.lootPool[collection] = chance

    def roll(self):
        collections = list(self.lootPool.keys())
        weights = list(self.lootPool.values())
        rolled_collection = random.choices(collections, weights=weights, k=1)[0]
        rolled_item = random.choice(rolled_collection.items)
        return rolled_item
