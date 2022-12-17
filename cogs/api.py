import discord
from discord.ext import tasks, commands


class API(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(API(bot))
    print("API Cog loaded")


async def teardown(bot):
    print("API Cog unloaded")
    await bot.remove_cog(API(bot))
