import discord
from discord.ext import tasks, commands


class Dig(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Dig(bot))
    print("Dig Cog loaded")


async def teardown(bot):
    print("Dig Cog unloaded")
    await bot.remove_cog(Dig(bot))
