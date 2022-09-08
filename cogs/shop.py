import discord
from discord.ext import tasks, commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Shop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Shop(bot))
    print("Shop Cog loaded")


async def teardown(bot):
    print("Shop Cog unloaded")
    await bot.remove_cog(Shop(bot))
