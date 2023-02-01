from datetime import datetime

import discord
from discord.ext import tasks, commands

import SharkBot


class Leaderboard(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.upload_loop.start()

    def cog_unload(self) -> None:
        self.upload_loop.cancel()

    @tasks.loop(seconds=30)
    async def upload_loop(self):
        db_log_channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Database Log"])
        message = await db_log_channel.send("Checking Leaderboards...")
        num = 0
        start = datetime.utcnow()
        for leaderboard in SharkBot.Leaderboard.Leaderboard.leaderboards:
            snapshot = leaderboard.create_current()
            if leaderboard.has_changed(snapshot):
                leaderboard.upload()
                leaderboard.save_snapshot(snapshot)
                num += 1
        end = datetime.utcnow()
        await message.edit(content=f"Done! Checking took {(end-start).total_seconds()}s. {num} changes detected.")

    @upload_loop.before_loop
    async def before_upload(self):
        await self.bot.wait_until_ready()

    @upload_loop.error
    async def update_db_error(self, error: Exception):
        await SharkBot.Utils.task_loop_handler(self.bot, error)

    @commands.command()
    @commands.is_owner()
    async def force_lb_upload(self, ctx: commands.Context):
        message = await ctx.send("Fetching Member Discord Users...")
        for member in SharkBot.Member.members:
            if member.discord_user is None:
                await member.fetch_discord_user(self.bot)
        await message.edit(content="Uploading Leaderboards...")
        for leaderboard in SharkBot.Leaderboard.Leaderboard.leaderboards:
            leaderboard.upload()
            leaderboard.save_snapshot()
        await message.edit(content="Done!")

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context, *, lb: SharkBot.Leaderboard.Leaderboard):
        member = SharkBot.Member.get(ctx.author.id)
        lb_snapshot = lb.create_ranked()

        embed = discord.Embed()
        embed.title = f"{lb.name} Leaderboard"
        content = []
        for lb_member in lb_snapshot:
            if lb_member.value == 0:
                continue
            if lb_member.member.discord_user is None:
                await lb_member.member.fetch_discord_user(self.bot)
            content.append(f"{lb_member.rank}. {lb_member.member_display_name} - {lb_member.value}")
            if lb_member.member == member:
                content[-1] = f"**{content[-1]}**"
        embed.description = "\n".join(content)
        await ctx.reply(embed=embed, mention_author=False)



async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
    print("Leaderboard Cog loaded")


async def teardown(bot):
    print("Leaderboard Cog unloaded")
    await bot.remove_cog(Leaderboard(bot))
