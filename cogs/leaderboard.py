import discord
from discord.ext import tasks, commands

import SharkBot


class Leaderboard(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.upload_loop.start()

    def cog_unload(self) -> None:
        self.upload_loop.cancel()

    @tasks.loop(seconds=5)
    async def upload_loop(self):
        for leaderboard in SharkBot.Leaderboard.Leaderboard.leaderboards:
            snapshot = leaderboard.create_current()
            if leaderboard.has_changed(snapshot):
                leaderboard.upload()
                leaderboard.save_snapshot(snapshot)


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
    print("Leaderboard Cog loaded")


async def teardown(bot):
    print("Leaderboard Cog unloaded")
    await bot.remove_cog(Leaderboard(bot))
