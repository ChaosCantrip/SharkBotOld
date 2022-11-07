import discord
from discord.ext import commands, tasks

import SharkBot


class ItemAdmin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ItemAdmin(bot))
    print("ItemAdmin Cog loaded")


async def teardown(bot):
    print("ItemAdmin Cog unloaded")
    await bot.remove_cog(ItemAdmin(bot))
