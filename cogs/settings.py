import discord
from discord.ext import tasks, commands

import SharkBot

class Settings(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("Settings Cog loaded")


async def teardown(bot):
    print("Settings Cog unloaded")
    await bot.remove_cog(Settings(bot))
