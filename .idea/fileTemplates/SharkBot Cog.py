import discord
from discord.ext import tasks, commands


class ${COG_NAME}(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(${COG_NAME}(bot))
    print("${COG_NAME} Cog loaded")


async def teardown(bot):
    print("${COG_NAME} Cog unloaded")
    await bot.remove_cog(${COG_NAME}(bot))