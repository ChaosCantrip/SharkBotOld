import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta

import SharkBot


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
        SharkBot.ZIPBackup.delete_backup(dt - timedelta(days=7))



async def setup(bot):
    await bot.add_cog(ZIPBackup(bot))
    print("ZIPBackup Cog loaded")


async def teardown(bot):
    print("ZIPBackup Cog unloaded")
    await bot.remove_cog(ZIPBackup(bot))
