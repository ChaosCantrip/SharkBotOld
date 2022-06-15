import discord.utils.get

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
