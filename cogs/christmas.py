import discord
from discord.ext import tasks, commands

import SharkBot


class Christmas(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Christmas(bot))
    print("Christmas Cog loaded")


async def teardown(bot):
    print("Christmas Cog unloaded")
    await bot.remove_cog(Christmas(bot))
