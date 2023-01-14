from typing import Union, Optional

import discord

from SharkBot import Errors, Icon
import SharkBot


class Collection:

    def __init__(self, collection_id: str, name: str, icon_name: str, colour: Union[discord.Colour, int],
                 xp_value: int, item_index_offset: int) -> None:
        self.id = collection_id
        self.name = name
        self._icon_name = icon_name
        self.colour = colour
        self.items: list[SharkBot.Item.Item] = []
        self.xp_value = xp_value
        self.item_index_offset = item_index_offset

    def __repr__(self) -> str:
        return f"Collection[id='{self.id}', name='{self.name}', items='{len(self.items)}']"

    def __str__(self) -> str:
        return f"{self.icon}  {self.name} Collection"

    def __len__(self) -> int:
        return len(self.items)

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


common = Collection("C", "Common", "common_item", discord.Color.light_grey(), 3, 0)
uncommon = Collection("U", "Uncommon", "uncommon_item", discord.Color.green(), 5, 100)
rare = Collection("R", "Rare", "rare_item", 0x6fa8dc, 10, 200)
legendary = Collection("L", "Legendary", "legendary_item", discord.Color.dark_purple(), 15, 300)
exotic = Collection("E", "Exotic", "exotic_item", discord.Color.gold(), 25, 400)
mythic = Collection("M", "Mythic", "mythic_item", discord.Color.red(), 50, 500)

lootboxes = Collection("LOOT", "Lootboxes", "lootboxes_item", discord.Color.orange(), 10, 600)
consumables = Collection("CON", "Consumables", "consumables_item", discord.Color.yellow(), 10, 700)

valentines = Collection("LOVE", "Valentines", "valentines_item", 0xfb00ff, 5, 800)
witch_queen = Collection("WQ", "Witch Queen", "witch_queen_item", 0x758B72, 5, 900)
easter = Collection("EA", "Easter", "easter_item", 0xF8E27F, 5, 1000)
summer = Collection("S", "Summer", "summer_item", 0xFDFBD3, 5, 1100)
slime_rancher = Collection("SR", "Slime Rancher", "slime_rancher_item", 0xEA1F96, 5, 1200)
halloween = Collection("H", "Halloween", "halloween_item", discord.Colour.dark_orange(), 5, 1300)
christmas = Collection("CH", "Christmas", "christmas_item", discord.Colour.dark_green(), 5, 1400)
new_year = Collection("NY", "New Year", "new_year_item", discord.Color.gold(), 5, 1500)
fragment = Collection("F", "Fragment", "fragment_item", discord.Colour.blurple(), 100, 10000)

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
    fragment
]


def get(search: str) -> Collection:
    search = search.upper()
    for collection in collections:
        if search == collection.id or search == collection.name.upper():
            return collection
    raise Errors.CollectionNotFoundError(search)
