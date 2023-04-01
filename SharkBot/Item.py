from datetime import datetime
from typing import Union, Optional, Self

import discord

import SharkBot.Collection
from SharkBot import Collection, Rarity, Errors, Lootpool, Utils


class Item:

    def __init__(self, item_id: str, name: str, description: str, collection: Collection.Collection,
                 rarity: Rarity.Rarity):
        self.id = item_id
        self.name = "The April Fool"
        self.description = "\n".join(description.split("[n]"))
        self.collection = collection
        self.rarity = rarity
        self.sellable = True
        self.type = "Item"
        self.xp_value = self.collection.xp_value
        self.item_index = len(items_dict)

    def __repr__(self) -> str:
        return f"Item[id={self.id}, name={self.name}, collection={self.collection.name}, rarity={self.rarity.name}]"

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"

    def __eq__(self, other: Self):
        return self.id == other.id

    def __hash__(self):
        return self.item_index

    def __lt__(self, other: Self):
        return self.item_index < other.item_index

    @property
    def icon(self) -> str:
        return self.rarity.icon

    def register(self) -> None:
        items_dict[self.id] = self
        self.collection.add_item(self)

    @property
    def embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.title = self.name
        embed.description = self.description
        embed.colour = self.collection.colour
        embed.set_footer(text=f"{self.type} | {self.rarity.name} | {self.id}")
        embed.set_thumbnail(url=self.rarity.icon_url)

        if self.sellable:
            embed.add_field(
                name="Sell Value",
                value=f"${self.value}"
            )
        else:
            embed.add_field(
                name="Sell Value",
                value="This Item cannot be sold."
            )
        embed.add_field(
            name="XP Value",
            value=f"`{self.xp_value} xp`"
        )


        return embed

    @property
    def value(self) -> int:
        return self.rarity.value

    @property
    def found_in(self):
        return [lootbox for lootbox in SharkBot.Collection.lootboxes.items if self in lootbox.lootPool.possible_items()]

    @property
    def db_data(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "icon_url": self.rarity.icon_url,
            "sellable": self.sellable,
            "collection": self.collection.db_data_lite,
            "rarity": self.rarity.name,
            "xp_value": self.xp_value,
            "value": self.value,
            "found_in": [
                lootbox.db_data_lite for lootbox in self.found_in
            ]
        }

    @property
    def db_data_lite(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon_url": self.rarity.icon_url
        }


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

    @classmethod
    def get(cls, lootbox_id: str) -> Self:
        lootbox_id = lootbox_id.upper()
        for lootbox in Collection.lootboxes:
            if lootbox.id == lootbox_id:
                return lootbox
        else:
            item = get(lootbox_id)
            if item is None:
                raise Errors.ItemIsNotLootboxError(lootbox_id.title(), item)

    @classmethod
    def search(cls, lootbox_search: str) -> Self:
        lootbox_search = lootbox_search.upper()
        for lootbox in Collection.lootboxes:
            if lootbox.id == lootbox_search or lootbox.name.upper() == lootbox_search:
                return lootbox
        else:
            item = search(lootbox_search)
            if item is None:
                raise Errors.ItemIsNotLootboxError(lootbox_search.title(), item)

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
        self.type = item.type
        self.sellable = item.sellable
        if self.id == "F1":
            self.description = "sbf1.chaoscantrip.com"
        elif self.id == "F2":
            self.description = "os.sharkbot.online"


class Consumable(Item):

    def __init__(self, item_id: str, name: str, description: str, icon: str):
        super().__init__(item_id, name, description, Collection.consumables, Rarity.consumables)
        self.sellable = False
        self.type = "Consumable"
        self._icon = icon

    @property
    def icon(self) -> str:
        return f":{self._icon}:"

    @classmethod
    def get(cls, consumable_id: str) -> Self:
        consumable_id = consumable_id.upper()
        for lootbox in Collection.lootboxes:
            if lootbox.id == consumable_id:
                return lootbox
        else:
            item = get(consumable_id)
            if item is None:
                raise Errors.ItemIsNotConsumableError(consumable_id.title(), item)

    @classmethod
    def search(cls, search_string: str) -> Self:
        search_string = search_string.upper()
        for consumable in Collection.consumables:
            if consumable.id == search_string or consumable.name.upper() == search_string:
                return consumable
        else:
            item = search(search_string)
            if item is None:
                raise Errors.ItemIsNotConsumableError(search_string.title(), item)


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
    item = items_dict.get(item_id)
    if item is not None:
        return item
    else:
        if item_id in converters:
            return get(converters[item_id])
        else:
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
    cons_split = search_string.split(" ")
    cons_split[-1] = f"({cons_split[-1]})"
    cons_search = " ".join(cons_split)
    for item in Collection.consumables.items:
        if cons_search == item.name.upper():
            return item
    if search_string in converters:
        return get(converters[search_string])
    close_matches = Utils.get_similar_items(search_string, cutoff=0.7)
    if close_matches is not None:
        return search(close_matches)
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

def import_consumables_file(filename: str) -> None:
    with open(filename, "r") as infile:
        raw_file_data = infile.read()

    item_data_set = [line.split("|") for line in raw_file_data.split("\n") if line != ""]

    for item_data in item_data_set:
        item = Consumable(
            item_id=item_data[0],
            name=item_data[1],
            description=item_data[2],
            icon=item_data[3]
        )

        item.register()

items_dict: dict[str, Union[Item, Lootbox, TimeLockedLootbox]] = {}

for filepath in Utils.get_dir_filepaths("data/static/collectibles/items"):
    import_item_file(filepath)

for filepath in Utils.get_dir_filepaths("data/static/collectibles/lootboxes/unlocked"):
    import_lootbox_file(filepath)

for filepath in Utils.get_dir_filepaths("data/static/collectibles/lootboxes/locked/time"):
    import_time_locked_lootbox_file(filepath)

for filepath in Utils.get_dir_filepaths("data/static/collectibles/consumables"):
    import_consumables_file(filepath)

items = list(items_dict.values())
items.sort()
item_lookup = [item.id for item in items] + [item.name for item in items]

load_converters()

guaranteed_new_boxes = ["LOOTM"]

current_event_box_ids: Optional[list[str]] = ["LOOTLF"]
current_event_boxes: Optional[list[Lootbox]] = None
if current_event_box_ids is not None:
    current_event_boxes = [get(event_box_id) for event_box_id in current_event_box_ids]

