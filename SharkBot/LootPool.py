from SharkBot import Collection
import random


class LootPool:

    def __init__(self, lootPoolCode):
        lootPoolCodes = lootPoolCode.split(";")
        self.lootPool = {}
        for code in lootPoolCodes:
            splitCode = code.split(":")
            collection = Collection.get(splitCode[0])
            chance = int(splitCode[1])
            self.lootPool[collection] = chance

    def roll(self):
        collections = list(self.lootPool.keys())
        weights = list(self.lootPool.values())
        rolledCollection = random.choices(collections, weights=weights, k=1)[0]
        rolledItem = random.choice(rolledCollection.items)
        return rolledItem
