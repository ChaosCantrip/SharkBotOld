import discord
from discord.ext import tasks, commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Missions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog loaded")


async def teardown(bot):
    print("Missions Cog unloaded")
    await bot.remove_cog(Missions(bot))
