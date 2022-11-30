import discord
from discord.ext import tasks, commands


class Levels(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Levels(bot))
    print("Levels Cog loaded")


async def teardown(bot):
    print("Levels Cog unloaded")
    await bot.remove_cog(Levels(bot))
