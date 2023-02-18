import logging

import discord
from discord.ext import commands

import SharkBot

command_logger = logging.getLogger("command")

import logging

cog_logger = logging.getLogger("cog")

class Logger(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        command_logger.info(f"{ctx.author.id} {ctx.author.display_name} - ${ctx.command.name} ({ctx.message.content})")

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