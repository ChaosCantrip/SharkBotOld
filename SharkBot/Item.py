from typing import Union

import discord
from SharkBot import Collection, Rarity, SharkErrors, LootPool


class Item:

    def __init__(self, itemDataString: str) -> None:
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.get(itemData[3])
        self.rarity = Rarity.get(itemData[3])

        self.collection.add_item(self)

    @property
    def embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.title = self.name
        embed.colour = self.collection.colour
        embed.description = self.description
        embed.set_footer(text=f"{self.rarity.name} | {self.id}")

        return embed

    @property
    def value(self) -> int:
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
        self.lootPool = LootPool.LootPool(itemData[4])

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


converters = {}


def load_converters() -> None:
    global converters
    with open("data/static/collectibles/converters.txt", "r") as infile:
        converters = {line[0]: line[1] for line in [line.split(":") for line in infile.read().split("\n")]}


def get(searchString: str) -> Union[Item, Lootbox]:
    searchString = searchString.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if searchString == item.id:
                return item
    if searchString in converters:
        return get(converters[searchString])
    raise SharkErrors.ItemNotFoundError(searchString)


def search(searchString: str) -> Union[Item, Lootbox]:
    searchString = searchString.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if searchString == item.id or searchString == item.name.upper():
                return item
    for item in Collection.lootboxes.items:
        if searchString + " LOOTBOX" == item.name.upper():
            return item
    if searchString in converters:
        return get(converters[searchString])
    raise SharkErrors.ItemNotFoundError(searchString)


def get_order_index(item: Union[str, Item]) -> int:
    if type(item) == str:
        item = get(item)

    return items.index(item)


def import_item_file(filename: str, itemType: type) -> None:
    with open(f"data/static/collectibles/items/{filename}", "r") as infile:
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

load_converters()

currentEventBoxID = None
if currentEventBoxID is None:
    currentEventBox = None
else:
    currentEventBox = get(currentEventBoxID)
