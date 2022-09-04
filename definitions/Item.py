from typing import Union

import discord
from definitions import Collection, Rarity, SharkErrors, LootPool


class Item:

    def __init__(self, itemDataString: str) -> None:
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.get(itemData[3])
        self.rarity = Rarity.get(itemData[3])

        self.collection.add_item(self)

    def generate_embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.title = self.name
        embed.colour = self.collection.colour
        embed.description = self.description
        embed.set_footer(text=f"{self.rarity.name} | {self.id}")

        return embed

    def get_value(self) -> int:
        return self.rarity.value

    @property
    def text(self) -> str:
        return f"{self.rarity.icon} {self.name}"


class Lootbox(Item):

    def __init__(self, itemDataString: str) -> None:
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.lootboxes
        self.rarity = Rarity.get(itemData[3])
        self.value = int(itemData[4])
        self.lootPool = LootPool.LootPool(itemData[5])

        self.collection.add_item(self)

    def roll(self) -> Item:
        return self.lootPool.roll()


class FakeItem(Item):

    def __init__(self, item: Item) -> None:
        self.id = item.id
        self.name = "???"
        self.description = "???"
        self.collection = item.collection
        self.rarity = item.rarity


def get(search: str) -> Union[Item, Lootbox]:
    search = search.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search == item.id:
                return item
    raise SharkErrors.ItemNotFoundError(search)


def search(search: str) -> Union[Item, Lootbox]:
    search = search.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search == item.id or search == item.name.upper():
                return item
    for item in Collection.lootboxes.items:
        if search + " LOOTBOX" == item.name.upper():
            return item
    raise SharkErrors.ItemNotFoundError(search)


def get_order_index(item: Union[str, Item]) -> int:
    if type(item) == str:
        item = get(item)

    return items.index(item)


def import_item_file(filename: str, itemType: type) -> None:
    with open(f"collectibles/{filename}", "r") as infile:
        fileData = infile.read()

    for line in fileData.split("\n"):
        if line == "":
            continue
        items.append(itemType(line))


items = []

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
import_item_file("summer.txt", Item)

currentEventBoxID = None
if currentEventBoxID is None:
    currentEventBox = None
else:
    currentEventBox = get(currentEventBoxID)
