import discord
from discord.ext import tasks, commands


class Redeem(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Redeem(bot))
    print("Redeem Cog loaded")


async def teardown(bot):
    print("Redeem Cog unloaded")
    await bot.remove_cog(Redeem(bot))
