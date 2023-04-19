import discord
from discord.ext import tasks, commands

import SharkBot


class VexTest(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(VexTest(bot))
    print("VexTest Cog loaded")


async def teardown(bot):
    print("VexTest Cog unloaded")
    await bot.remove_cog(VexTest(bot))
