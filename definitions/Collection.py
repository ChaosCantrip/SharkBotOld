import discord.utils.get, discord.Color

from definitions import SharkErrors

import secret
if secret.testBot:
    import testids as ids
else:
    import ids

class Collection():
    
    def __init__(self, id, name, iconName, colour):
        self.id = id
        self.name = name
        self.iconName = iconName
        self.icon = None
        self.colour = colour
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    async def get_icon(self, bot):
        if self.icon == None:
            server = await bot.fetch_guild(ids.server)
            self.icon = discord.utils.get(server.emojis, name=self.iconName)
        return self.icon

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
    easter
]

def get(search: str):
    search = search.upper()
    for collection in collections:
        if search == collection.id or search == collection.name.upper():
            return collection
    raise SharkErrors.CollectionNotFoundError(search)
