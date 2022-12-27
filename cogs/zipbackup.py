import discord
from discord.ext import commands
from datetime import datetime

import SharkBot


class ZIPBackup(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def take_backup(self, ctx: commands.Context):
        await ctx.reply("Creating backup...")
        dt = datetime.now().date()
        SharkBot.ZIPBackup.create_backup(dt)
        await SharkBot.ZIPBackup.send_backup(ctx, dt)



async def setup(bot):
    await bot.add_cog(ZIPBackup(bot))
    print("ZIPBackup Cog loaded")


async def teardown(bot):
    print("ZIPBackup Cog unloaded")
    await bot.remove_cog(ZIPBackup(bot))
