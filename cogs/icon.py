import discord
from discord.ext import commands

import SharkBot


class Icon(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Icon(bot))
    print("Icon Cog loaded")


async def teardown(bot):
    print("Icon Cog unloaded")
    await bot.remove_cog(Icon(bot))
