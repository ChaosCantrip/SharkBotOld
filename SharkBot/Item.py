from datetime import datetime
from typing import Union

import discord
from SharkBot import Collection, Rarity, Errors, Lootpool, Utils


class Item:

    def __init__(self, item_id: str, name: str, description: str, collection: Collection.Collection,
                 rarity: Rarity.Rarity):
        self.id = item_id
        self.name = name
        self.description = description
        self.collection = collection
        self.rarity = rarity
        self.sellable = True
        self.type = "Item"
        self.xp_value = self.collection.xp_value
        self.item_index = self.collection.item_index_offset + len(self.collection)

    def __repr__(self) -> str:
        return f"Item[id={self.id}, name={self.name}, collection={self.collection.name}, rarity={self.rarity.name}]"

    def __str__(self) -> str:
        return f"{self.rarity.icon} {self.name}"

    def register(self) -> None:
        items.append(self)
        self.collection.add_item(self)

    @property
    def embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.title = self.name
        embed.colour = self.collection.colour
        embed.set_footer(text=f"{self.rarity.name} | {self.id}")

        embed.add_field(
            name="Description",
            value=self.description,
            inline=False
        )
        embed.add_field(
            name="Sell Value",
            value=self.value,
            inline=False
        )

        return embed

    @property
    def value(self) -> int:
        return self.rarity.value


class Lootbox(Item):

    def __init__(self, item_id: str, name: str, description: str, collection: Collection, rarity: Rarity) -> None:

        super().__init__(item_id, name, description, collection, rarity)
        self.lootPool = Lootpool.get(self.id)
        self.sellable = False
        self.type = "Lootbox"

    def _check_unlocked(self) -> bool:
        return True

    @property
    def locked(self) -> bool:
        return not self._check_unlocked()

    @property
    def unlocked(self) -> bool:
        return self._check_unlocked()

    def roll(self) -> Item:
        return self.lootPool.roll()


class TimeLockedLootbox(Lootbox):

    def __init__(self, item_id: str, name: str, description: str, collection: Collection, rarity: Rarity,
                 unlock_dt: str):
        super().__init__(item_id, name, description, collection, rarity)
        self.unlock_dt = datetime.strptime(unlock_dt, "%d/%m/%Y-%H:%M:%S")

    def _check_unlocked(self) -> bool:
        return datetime.now() > self.unlock_dt


class FakeItem(Item):

    def __init__(self, item: Item) -> None:
        super().__init__(
            item_id=item.id,
            name="???",
            description="???",
            collection=item.collection,
            rarity=item.rarity
        )
        if self.id == "F1":
            self.description = "sbf1.chaoscantrip.com"


converters = {}


def load_converters() -> None:
    global converters
    with open("data/static/collectibles/converters.txt", "r") as infile:
        converters = {line[0]: line[1] for line in [line.split(":") for line in infile.read().split("\n")]}


def get(item_id: str) -> Union[Item, Lootbox, TimeLockedLootbox]:
    """
    Fetches the Item with the given Item ID

    :param item_id: The Item ID to search with
    :return: The Item with the given ID
    """

    item_id = item_id.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if item_id == item.id:
                return item
    if item_id in converters:
        return get(converters[item_id])
    raise Errors.ItemNotFoundError(item_id)


def search(search_string: str) -> Union[Item, Lootbox, TimeLockedLootbox]:
    """
    Fetches the Item with the given Item ID or Name

    :param search_string: The string to search with
    :return: The Item with the given ID or Name
    """

    search_string = search_string.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search_string == item.id or search_string == item.name.upper():
                return item
    for item in Collection.lootboxes.items:
        if search_string + " LOOTBOX" == item.name.upper():
            return item
    if search_string in converters:
        return get(converters[search_string])
    raise Errors.ItemNotFoundError(search_string)


def get_order_index(item: Union[str, Item]) -> int:
    if type(item) == str:
        item = get(item)

    return item.item_index


def import_item_file(filename: str) -> None:
    with open(filename, "r") as infile:
        raw_file_data = infile.read()

    item_data_set = [line.split("|") for line in raw_file_data.split("\n") if line != ""]

    for item_data in item_data_set:
        item = Item(
            item_id=item_data[0],
            name=item_data[1],
            description=item_data[2],
            collection=Collection.get(item_data[3]),
            rarity=Rarity.get(item_data[3])
        )

        item.register()


def import_lootbox_file(filename: str) -> None:
    with open(filename, "r") as infile:
        raw_file_data = infile.read()

    item_data_set = [line.split("|") for line in raw_file_data.split("\n") if line != ""]

    for item_data in item_data_set:
        item = Lootbox(
            item_id=item_data[0],
            name=item_data[1],
            description=item_data[2],
            collection=Collection.lootboxes,
            rarity=Rarity.get(item_data[3])
        )

        item.register()


def import_time_locked_lootbox_file(filename: str) -> None:
    with open(filename, "r") as infile:
        raw_file_data = infile.read()

    item_data_set = [line.split("|") for line in raw_file_data.split("\n") if line != ""]

    for item_data in item_data_set:
        item = TimeLockedLootbox(
            item_id=item_data[0],
            name=item_data[1],
            description=item_data[2],
            collection=Collection.lootboxes,
            rarity=Rarity.get(item_data[3]),
            unlock_dt=item_data[4]
        )

        item.register()


items = []

for filepath in Utils.get_dir_filepaths("data/static/collectibles/items"):
    import_item_file(filepath)

for filepath in Utils.get_dir_filepaths("data/static/collectibles/lootboxes/unlocked"):
    import_lootbox_file(filepath)

for filepath in Utils.get_dir_filepaths("data/static/collectibles/lootboxes/locked/time"):
    import_time_locked_lootbox_file(filepath)

load_converters()

guaranteed_new_boxes = ["LOOTM"]

currentEventBoxID: Union[str, None] = "LOOTNY"
if currentEventBoxID is None:
    currentEventBox = None
else:
    currentEventBox = get(currentEventBoxID)
