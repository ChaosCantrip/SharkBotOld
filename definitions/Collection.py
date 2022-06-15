import discord.utils.get, discord.Color

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

    async def get_icon(self, bot):
        if self.icon == None:
            server = await bot.fetch_guild(ids.server)
            self.icon = discord.utils.get(server.emojis, name=self.iconName)
        return self.icon

common = Collection("C", "common", "common_item", discord.Color.light_grey())
uncommon = Collection("U", "uncommon", "uncommon_item", discord.Color.green())
rare = Collection("R", "rare", "rare_item", 0x6fa8dc)
legendary = Collection("L", "legendary", "legendary_item", discord.Color.dark_purple())
exotic = Collection("E", "exotic", "exotic_item", discord.Color.gold())
mythic = Collection("M", "mythic", "mythic_item", discord.Color.red())

lootboxes = Collection("LOOT", "lootboxes", "lootboxes_item", discord.Color.orange())

valentines = Collection("LOVE", "valentines", "valentines_item", 0xfb00ff)
witch_queen = Collection("WQ", "witch queen", "witch queen_item", 0x758B72)
easter = Collection("EA", "easter", "easter_item", 0xF8E27F)

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