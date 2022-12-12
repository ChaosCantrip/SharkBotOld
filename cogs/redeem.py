import discord
from discord.ext import tasks, commands


class Redeem(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def redeem(self, ctx: commands.Context, code: str):
        embed = discord.Embed()
        embed.title = "Redeem"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Redeem(bot))
    print("Redeem Cog loaded")


async def teardown(bot):
    print("Redeem Cog unloaded")
    await bot.remove_cog(Redeem(bot))
