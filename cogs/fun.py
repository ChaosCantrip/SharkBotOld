import discord
from discord.ext import tasks, commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Fun(bot))
    print("Fun Cog loaded")


async def teardown(bot):
    print("Fun Cog unloaded")
    await bot.remove_cog(Fun(bot))
