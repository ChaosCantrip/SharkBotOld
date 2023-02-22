from typing import Union

import discord

import SharkBot
from SharkBot import Errors, Icon


class Collection:

    def __init__(self, collection_id: str, name: str, icon_name: str,
                 colour: Union[discord.Colour, int], xp_value: int) -> None:
        self.id = collection_id
        self.name = name
        self._icon_name = icon_name
        self.colour = colour
        self.items: list[SharkBot.Item.Item] = []
        self.xp_value = xp_value

    def __repr__(self) -> str:
        return f"Collection[id='{self.id}', name='{self.name}', items='{len(self.items)}']"

    def __str__(self) -> str:
        return f"{self.icon}  {self.name} Collection"

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, item) -> bool:
        return item in self.items

    @property
    def icon(self) -> str:
        return Icon.get(self._icon_name)

    def add_item(self, item) -> None:
        self.items.append(item)

    @property
    def length(self) -> int:
        return len(self.items)

    @property
    def icon_url(self) -> str:
        icon_id = self.icon.split(":")[-1][:-1]
        return f"https://cdn.discordapp.com/emojis/{icon_id}.png"

    @property
    def db_data(self) -> dict:
        return {
            "id": self.id,
            "index": collections.index(self),
            "name": self.name,
            "icon_url": self.icon_url,
            "xp_value": self.xp_value,
            "num_items": len(self),
            "items": [
                item.db_data_lite for item in self.items
            ]
        }

    @property
    def db_data_lite(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "icon_url": self.icon_url,
            "num_items": len(self)
        }


common = Collection("C", "Common", "common_item", discord.Color.light_grey(), 3)
uncommon = Collection("U", "Uncommon", "uncommon_item", discord.Color.green(), 5)
rare = Collection("R", "Rare", "rare_item", 0x6fa8dc, 10)
legendary = Collection("L", "Legendary", "legendary_item", discord.Color.dark_purple(), 15)
exotic = Collection("E", "Exotic", "exotic_item", discord.Color.gold(), 25)
mythic = Collection("M", "Mythic", "mythic_item", discord.Color.red(), 50)

lootboxes = Collection("LOOT", "Lootboxes", "lootboxes_item", discord.Color.orange(), 10)
consumables = Collection("CON", "Consumables", "consumables_item", discord.Color.yellow(), 10)

valentines = Collection("LOVE", "Valentines", "valentines_item", 0xfb00ff, 5)
witch_queen = Collection("WQ", "Witch Queen", "witch_queen_item", 0x758B72, 5)
easter = Collection("EA", "Easter", "easter_item", 0xF8E27F, 5)
summer = Collection("S", "Summer", "summer_item", 0xFDFBD3, 5)
slime_rancher = Collection("SR", "Slime Rancher", "slime_rancher_item", 0xEA1F96, 5)
halloween = Collection("H", "Halloween", "halloween_item", discord.Colour.dark_orange(), 5)
christmas = Collection("CH", "Christmas", "christmas_item", discord.Colour.dark_green(), 5)
new_year = Collection("NY", "New Year", "new_year_item", discord.Color.gold(), 5)
lunar_new_year = Collection("LNY", "Lunar New Year", "lunarnewyear_item", discord.Color.red(), 5)
zodiac = Collection("Z", "Zodiac", "zodiac_item", discord.Color.dark_purple(), 5)
anniversary = Collection("A", "Anniversary", "anniversary_item", discord.Color.dark_gold(), 7)
timelost = Collection("TL", "Timelost", "timelost_item", discord.Color.dark_gold(), 5)
perfected = Collection("P", "Perfected", "perfected_item", discord.Color.dark_gold(), 5)

fragment = Collection("F", "Fragment", "fragment_item", discord.Colour.blurple(), 100)

collections = [
    common,
    uncommon,
    rare,
    legendary,
    exotic,
    mythic,
    lootboxes,
    consumables,
    valentines,
    witch_queen,
    easter,
    summer,
    slime_rancher,
    halloween,
    christmas,
    new_year,
    lunar_new_year,
    zodiac,
    anniversary,
    timelost,
    perfected,
    fragment
]

_collections_dict: dict[str, Collection] = {
    collection.id: collection for collection in collections
}


def get(search: str) -> Collection:
    search = search.upper()
    collection = _collections_dict.get(search)
    if collection is not None:
        return collection
    for collection in collections:
        if search == collection.name.upper():
            return collection
    else:
        raise Errors.CollectionNotFoundError(search)
