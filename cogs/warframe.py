import discord
from discord.ext import tasks, commands


class Warframe(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group()
    async def warframe(self, ctx: commands.Context) -> None:
        await ctx.send_help(self.warframe)


async def setup(bot):
    await bot.add_cog(Warframe(bot))
    print("Warframe Cog loaded")


async def teardown(bot):
    print("Warframe Cog unloaded")
    await bot.remove_cog(Warframe(bot))
