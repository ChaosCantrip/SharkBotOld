import discord
from discord.ext import tasks, commands
import logging

class Logger(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Logger(bot))
    print("Logger Cog loaded")


async def teardown(bot):
    print("Logger Cog unloaded")
    await bot.remove_cog(Logger(bot))
