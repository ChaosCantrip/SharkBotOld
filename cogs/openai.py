import discord
from discord.ext import tasks, commands


class OpenAI(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(OpenAI(bot))
    print("OpenAI Cog loaded")


async def teardown(bot):
    print("OpenAI Cog unloaded")
    await bot.remove_cog(OpenAI(bot))
