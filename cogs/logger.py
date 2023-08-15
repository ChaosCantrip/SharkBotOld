import logging
from datetime import datetime

import discord
from discord.ext import commands

import SharkBot

command_logger = logging.getLogger("command")
cog_logger = logging.getLogger("cog")

command_starts: dict[int, datetime] = {}
command_durations: dict[commands.Command, list[float]] = {}


def log_command_start(ctx: commands.Context):
    command_logger.info(f"{ctx.author.id} {ctx.author} - ${ctx.command.name} ({ctx.message.content}) - Started")
    command_starts[ctx.message.id] = datetime.utcnow()


def log_command_end(ctx: commands.Context):
    start = command_starts.pop(ctx.message.id)
    duration = (datetime.utcnow() - start).total_seconds()
    if ctx.command not in command_durations:
        command_durations[ctx.command] = []
    command_durations[ctx.command].append(duration)
    command_logger.info(f"{ctx.author.id} {ctx.author} - ${ctx.command.name} ({ctx.message.content}) - Completed - {duration}s")


class Logger(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        log_command_start(ctx)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        log_command_end(ctx)

    @commands.command()
    @commands.is_owner()
    async def get_log(self, ctx: commands.Context):
        await self.list_logs(ctx)
        log_names = []
        for filepath in SharkBot.Utils.get_dir_filepaths("data/live/bot/logs"):
            file = discord.File(filepath)
            log_names.append(file.filename)
            await ctx.reply(f"Log - {file.filename}", file=file, mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def list_logs(self, ctx: commands.Context):
        log_names = "\n".join(filepath.split("/")[-1] for filepath in SharkBot.Utils.get_dir_filepaths("data/live/bot/logs"))
        await ctx.reply(f"```Log Files:\n\n{log_names}```", mention_author=False)


async def setup(bot):
    await bot.add_cog(Logger(bot))
    print("Logger Cog Loaded")
    cog_logger.info("Logger Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Logger(bot))
    print("Logger Cog Unloaded")
    cog_logger.info("Logger Cog Unloaded")