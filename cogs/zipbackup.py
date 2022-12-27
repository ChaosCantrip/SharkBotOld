import discord
from discord.ext import commands

import SharkBot


class ZIPBackup(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ZIPBackup(bot))
    print("ZIPBackup Cog loaded")


async def teardown(bot):
    print("ZIPBackup Cog unloaded")
    await bot.remove_cog(ZIPBackup(bot))
