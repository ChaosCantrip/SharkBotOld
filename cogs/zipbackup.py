import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta

import SharkBot


import logging

cog_logger = logging.getLogger("cog")

class ZIPBackup(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.backup_loop.start()

    def cog_unload(self) -> None:
        self.backup_loop.cancel()

    @commands.command()
    @commands.is_owner()
    async def take_backup(self, ctx: commands.Context):
        await ctx.reply("Creating backup...")
        dt = datetime.now().date()
        SharkBot.ZIPBackup.create_backup(dt)
        await SharkBot.ZIPBackup.send_backup(ctx, dt)

    @tasks.loop(time=time(hour=6))
    async def backup_loop(self):
        channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Backups"])
        dt = datetime.now().date()
        SharkBot.ZIPBackup.create_backup(dt)
        await SharkBot.ZIPBackup.send_backup(channel, dt)
        try:
            SharkBot.ZIPBackup.delete_backup(dt - timedelta(days=7))
        except SharkBot.Errors.ZIPBackup.BackupDoesNotExistError:
            pass


async def setup(bot):
    await bot.add_cog(ZIPBackup(bot))
    print("ZIPBackup Cog Loaded")
    cog_logger.info("ZIPBackup Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(ZIPBackup(bot))
    print("ZIPBackup Cog Unloaded")
    cog_logger.info("ZIPBackup Cog Unloaded")