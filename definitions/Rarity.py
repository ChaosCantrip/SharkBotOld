from definitions import SharkErrors
import discord


class Rarity:

    def __init__(self, name, value, iconName):
        self.name = name
        self.value = value
        self.iconName = iconName
        self.icon = None

    def get_icon(self, server):
        if self.icon is None:
            self.icon = discord.utils.get(server.emojis, name=self.iconName)
        return self.icon


common = Rarity("Common", 5, "common_item")
uncommon = Rarity("Uncommon", 10, "uncommon_item")
rare = Rarity("Rare", 20, "rare_item")
legendary = Rarity("Legendary", 50, "legendary_item")
exotic = Rarity("Exotic", 150, "exotic_item")
mythic = Rarity("Mythic", 500, "mythic_item")

lootboxes = Rarity("Lootboxes", 100, "lootboxes_item")

valentines = Rarity("Valentines", 10, "valentines_item")
witch_queen = Rarity("Witch Queen", 10, "witch_queen_item")
easter = Rarity("Easter", 10, "easter_item")
summer = Rarity("Summer", 10, "summer_item")

rarities = [common, uncommon, rare, legendary, exotic, lootboxes, mythic, valentines, witch_queen, easter, summer]


def get(search: str):
    search = search.upper()
    for rarity in rarities:
        if search == rarity.name.upper():
            return rarity
    raise SharkErrors.RarityNotFoundError(search)
