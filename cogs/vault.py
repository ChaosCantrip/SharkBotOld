import discord
from discord.ext import tasks, commands


class Vault(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Vault(bot))
    print("Vault Cog loaded")


async def teardown(bot):
    print("Vault Cog unloaded")
    await bot.remove_cog(Vault(bot))
