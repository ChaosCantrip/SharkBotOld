import discord
from discord.ext import tasks, commands
import logging

command_logger = logging.getLogger("command")

class Logger(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        command_logger.info(f"{ctx.message.created_at} - {ctx.author.id} - ${ctx.command.name}")


async def setup(bot):
    await bot.add_cog(Logger(bot))
    print("Logger Cog loaded")


async def teardown(bot):
    print("Logger Cog unloaded")
    await bot.remove_cog(Logger(bot))
