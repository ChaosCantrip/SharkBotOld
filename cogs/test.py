import discord
from discord.ext import commands, tasks

import SharkBot


class Test(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Test(bot))
    print("Test Cog loaded")


async def teardown(bot):
    print("Test Cog unloaded")
    await bot.remove_cog(Test(bot))
