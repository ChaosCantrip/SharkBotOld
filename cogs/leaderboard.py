import discord
from discord.ext import tasks, commands

import SharkBot


class Leaderboard(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
    print("Leaderboard Cog loaded")


async def teardown(bot):
    print("Leaderboard Cog unloaded")
    await bot.remove_cog(Leaderboard(bot))
