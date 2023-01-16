from typing import Optional

from SharkBot import Errors, Icon


class Rarity:

    def __init__(self, name: str, value: int, icon_name: str) -> None:
        self.name = name
        self.value = value
        self._icon_name: str = icon_name

    def __repr__(self) -> str:
        return f"Rarity[name='{self.name}', value='{self.value}', icon='{self._icon_name}']"

    def __str__(self) -> str:
        return f"{self.icon}  {self.name} Rarity"

    @property
    def icon(self) -> str:
        return Icon.get(self._icon_name)


common = Rarity("Common", 5, "common_item")
uncommon = Rarity("Uncommon", 10, "uncommon_item")
rare = Rarity("Rare", 20, "rare_item")
legendary = Rarity("Legendary", 50, "legendary_item")
exotic = Rarity("Exotic", 150, "exotic_item")
mythic = Rarity("Mythic", 500, "mythic_item")

lootboxes = Rarity("Lootboxes", 100, "lootboxes_item")
consumables = Rarity("Consumables", 100, "consumables_item")

valentines = Rarity("Valentines", 10, "valentines_item")
witch_queen = Rarity("Witch Queen", 10, "witch_queen_item")
easter = Rarity("Easter", 10, "easter_item")
summer = Rarity("Summer", 10, "summer_item")
slime_rancher = Rarity("Slime Rancher", 10, "slime_rancher_item")
halloween = Rarity("Halloween", 10, "halloween_item")
christmas = Rarity("Christmas", 10, "christmas_item")
new_year = Rarity("New Year", 10, "new_year_item")
lunar_new_year = Rarity("Lunar New Year", 10, "lunarnewyear_item")
zodiac = Rarity("Zodiac", 10, "zodiac_item")
fragment = Rarity("Fragment", 500, "fragment_item")

rarities = [
    common,
    uncommon,
    rare,
    legendary,
    exotic,
    lootboxes,
    consumables,
    mythic,
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
    fragment
]


def get(search: str) -> Rarity:
    search = search.upper()
    for rarity in rarities:
        if search == rarity.name.upper():
            return rarity
    raise Errors.RarityNotFoundError(search)
