from typing import ItemsView
import discord
from definitions import Collection, Rarity, SharkErrors, LootPool

class Item():
    
    def __init__(self, itemDataString):
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.get(itemData[3])
        self.rarity = Rarity.get(itemData[3])

        self.collection.add_item(self)

    def generate_embed(self):
        embed = discord.Embed()
        embed.title = self.name
        embed.color = self.collection.colour
        embed.description = self.description
        embed.set_footer(text = f"{self.rarity.name} | {self.id}")

        return embed

class Lootbox():
    
    def __init__(self, itemDataString):
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.lootboxes
        self.rarity = Rarity.get(itemData[3])
        self.value = int(itemData[4])
        self.lootPool = LootPool.LootPool(itemData[5])

        self.collection.add_item(self)

    def roll(self):
        return self.lootPool.roll()

def get(search: str):
    search = search.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search == item.id:
                return item
    raise SharkErrors.ItemNotFoundError(search)

def search(search: str):
    search = search.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search == item.id or search == item.name.upper():
                return item
    for item in Collection.lootboxes.items:
        if search + " LOOTBOX" == item.name.upper():
            return item
    raise SharkErrors.ItemNotFoundError(search)

items = []

def import_item_file(filename, itemType):
    with open(f"collectibles/{filename}", "r") as infile:
        fileData = infile.read()

    for line in fileData.split("\n"):
        if line == "":
            continue
        items.append(itemType(line))

import_item_file("common.txt", Item)
import_item_file("uncommon.txt", Item)
import_item_file("rare.txt", Item)
import_item_file("legendary.txt", Item)
import_item_file("exotic.txt", Item)
import_item_file("mythic.txt", Item)

import_item_file("lootboxes.txt", Lootbox)

import_item_file("valentines.txt", Item)
import_item_file("witch_queen.txt", Item)
import_item_file("easter.txt", Item)
