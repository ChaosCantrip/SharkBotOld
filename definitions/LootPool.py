from definitions import Collection.get
import random

class LootPool():
    
    def __init__(self, lootPoolCode):
        lootPoolCodes = lootPoolCode.split(";")
        lootPool = {}
        for code in lootPoolCodes:
            splitCode = code.split(":")
            collection = Collection.get(splitCode[0])
            chance = int(splitCode[1])
            lootPool[collection] = chance
