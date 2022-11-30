import discord
from discord.ext import tasks, commands

from SharkBot import Member


class Levels(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def level(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Level"
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.description = f"You are **Level {member.xp.level}** with `{member.xp.xp} xp`"

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Levels(bot))
    print("Levels Cog loaded")


async def teardown(bot):
    print("Levels Cog unloaded")
    await bot.remove_cog(Levels(bot))
