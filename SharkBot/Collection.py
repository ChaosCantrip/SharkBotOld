from typing import Union

import discord

from SharkBot import Errors, Icons


class Collection:

    def __init__(self, collectionID: str, name: str, iconName: str, colour: Union[discord.Colour, int]) -> None:
        self.id = collectionID
        self.name = name
        self.icon = Icons.Collections[iconName]
        self.colour = colour
        self.items = []

    def add_item(self, item) -> None:
        self.items.append(item)

    @property
    def length(self) -> int:
        return len(self.items)


common = Collection("C", "Common", "common_item", discord.Color.light_grey())
uncommon = Collection("U", "Uncommon", "uncommon_item", discord.Color.green())
rare = Collection("R", "Rare", "rare_item", 0x6fa8dc)
legendary = Collection("L", "Legendary", "legendary_item", discord.Color.dark_purple())
exotic = Collection("E", "Exotic", "exotic_item", discord.Color.gold())
mythic = Collection("M", "Mythic", "mythic_item", discord.Color.red())

lootboxes = Collection("LOOT", "Lootboxes", "lootboxes_item", discord.Color.orange())

valentines = Collection("LOVE", "Valentines", "valentines_item", 0xfb00ff)
witch_queen = Collection("WQ", "Witch Queen", "witch_queen_item", 0x758B72)
easter = Collection("EA", "Easter", "easter_item", 0xF8E27F)
summer = Collection("S", "Summer", "summer_item", 0xFDFBD3)

collections = [
    common,
    uncommon,
    rare,
    legendary,
    exotic,
    mythic,
    lootboxes,
    valentines,
    witch_queen,
    easter,
    summer
]


def get(search: str) -> Collection:
    search = search.upper()
    for collection in collections:
        if search == collection.id or search == collection.name.upper():
            return collection
    raise Errors.CollectionNotFoundError(search)
