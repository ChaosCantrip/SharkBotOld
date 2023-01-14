import discord
from discord.ext import tasks, commands


class Effects(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Effects(bot))
    print("Effects Cog loaded")


async def teardown(bot):
    print("Effects Cog unloaded")
    await bot.remove_cog(Effects(bot))
