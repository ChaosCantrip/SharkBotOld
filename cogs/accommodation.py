import discord
from discord.ext import tasks, commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Accommodation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Accommodation(bot))
    print("Accommodation Cog loaded")


async def teardown(bot):
    print("Accommodation Cog unloaded")
    await bot.remove_cog(Accommodation(bot))
