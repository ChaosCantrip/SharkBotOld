import discord
from discord.ext import tasks, commands

import SharkBot

_CONFIG_FILEPATH = "data/live/bungie/vex_test_config.json"
SharkBot.Utils.FileChecker.json(_CONFIG_FILEPATH, {
    "channel_id": None,
    "check_interval": 60,
    "report_interval": 3600,
    "running": False
})
_CONFIG = SharkBot.Utils.JSON.load(_CONFIG_FILEPATH)
_ACTIVITY_ID = 231808097


class VexTest(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.num = 0
        self.num_checks = 0
        if _CONFIG["running"]:
            self.check_loop.start()
            self.report_loop.start()

    @tasks.loop(seconds=_CONFIG["check_interval"])
    async def check_loop(self):
        dev_member = SharkBot.Member.get(SharkBot.IDs.dev)
        response = await dev_member.bungie.get_profile_response(204)
        activity_hashes = [
            activity["activityHash"] for activity in list(response["characterActivities"]["data"].values())[0]["availableActivities"]
        ]
        if _ACTIVITY_ID in activity_hashes:
            self.num += 1
        self.num_checks += 1

    @tasks.loop(seconds=_CONFIG["report_interval"])
    async def report_loop(self):
        channel = self.bot.get_channel(_CONFIG["channel_id"])
        if channel is None:
            channel = await self.bot.fetch_channel(_CONFIG["channel_id"])
        embed = discord.Embed()
        embed.title = "Vex Test Report"
        embed.description = f"```{self.num} Instances of Vex Offensive Found.\n{self.num_checks} Checks Performed.```"
        await channel.send(embed=embed)
        self.num = 0
        self.num_checks = 0

    @check_loop.before_loop
    async def before_check_loop(self):
        await self.bot.wait_until_ready()

    @report_loop.before_loop
    async def before_report_loop(self):
        await self.bot.wait_until_ready()

    @check_loop.error
    async def check_loop_error(self, error):
        await SharkBot.Utils.task_loop_handler(self.bot, error)
        self.check_loop.restart()

    @report_loop.error
    async def report_loop_error(self, error):
        await SharkBot.Utils.task_loop_handler(self.bot, error)
        self.report_loop.restart()

    @commands.hybrid_group(name="vex_test", aliases=["vt"])
    @SharkBot.Checks.is_mod()
    async def vex_test(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @vex_test.command(name="start")
    @SharkBot.Checks.is_mod()
    async def vex_test_start(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Vex Test"
        )
        if _CONFIG["running"]:
            embed.description = "Vex Test is already running."
            await ctx.send(embed=embed)
            return
        _CONFIG["channel_id"] = ctx.channel.id
        _CONFIG["running"] = True
        SharkBot.Utils.JSON.dump(_CONFIG_FILEPATH, _CONFIG)
        self.check_loop.start()
        self.report_loop.start()
        embed.description = "Vex Test started."
        embed.add_field(
            name="Check Interval",
            value=f"{_CONFIG['check_interval']} seconds"
        )
        embed.add_field(
            name="Report Interval",
            value=f"{_CONFIG['report_interval']} seconds"
        )
        await ctx.send(embed=embed)

    @vex_test.command(name="stop")
    @SharkBot.Checks.is_mod()
    async def vex_test_stop(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Vex Test"
        )
        if not _CONFIG["running"]:
            embed.description = "Vex Test is not running."
            await ctx.send(embed=embed)
            return
        _CONFIG["channel_id"] = None
        _CONFIG["running"] = False
        SharkBot.Utils.JSON.dump(_CONFIG_FILEPATH, _CONFIG)
        self.check_loop.stop()
        self.report_loop.stop()
        embed.description = "Vex Test stopped."
        await ctx.send(embed=embed)

    @vex_test.command(name="check_interval")
    @SharkBot.Checks.is_mod()
    async def vex_test_check_interval(self, ctx: commands.Context, interval: int):
        embed = discord.Embed(
            title="Vex Test"
        )
        if interval < 1:
            embed.description = "Interval must be at least 1 second."
            await ctx.send(embed=embed)
            return
        _CONFIG["check_interval"] = interval
        SharkBot.Utils.JSON.dump(_CONFIG_FILEPATH, _CONFIG)
        self.check_loop.change_interval(seconds=interval)
        embed.description = f"Vex Test check interval changed to {interval} seconds."
        await ctx.send(embed=embed)

    @vex_test.command(name="report_interval")
    @SharkBot.Checks.is_mod()
    async def vex_test_report_interval(self, ctx: commands.Context, interval: int):
        embed = discord.Embed(
            title="Vex Test"
        )
        if interval < 1:
            embed.description = "Interval must be at least 1 second."
            await ctx.send(embed=embed)
            return
        _CONFIG["report_interval"] = interval
        SharkBot.Utils.JSON.dump(_CONFIG_FILEPATH, _CONFIG)
        self.report_loop.change_interval(seconds=interval)
        embed.description = f"Vex Test report interval changed to {interval} seconds."
        await ctx.send(embed=embed)

    @vex_test.command(name="status")
    @SharkBot.Checks.is_mod()
    async def vex_test_status(self, ctx: commands.Context):
        if _CONFIG["channel_id"] is None:
            channel = None
        else:
            channel = self.bot.get_channel(_CONFIG["channel_id"])
            if channel is None:
                channel = await self.bot.fetch_channel(_CONFIG["channel_id"])
        if channel is None:
            channel = "None"
        else:
            channel = f"{channel.mention} ({channel.id})"
        embed = discord.Embed(
            title="Vex Test Status",
            color=discord.Color.blue()
        )
        embed.add_field(name="Channel", value=channel)
        embed.add_field(name="Check Interval", value=f"{_CONFIG['check_interval']} seconds")
        embed.add_field(name="Report Interval", value=f"{_CONFIG['report_interval']} seconds")
        embed.add_field(name="Running", value=_CONFIG["running"])
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VexTest(bot))
    print("VexTest Cog loaded")


async def teardown(bot):
    print("VexTest Cog unloaded")
    await bot.remove_cog(VexTest(bot))
