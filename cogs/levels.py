import discord
from discord.ext import tasks, commands

from SharkBot import Member, IDs


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

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def add_xp(self, ctx: commands.Context, target: discord.Member, amount: int):
        target_member = Member.get(target.id)
        await target_member.xp.add(amount, ctx)
        await ctx.reply(f"Added `{amount} xp` to {target.mention}")

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def set_xp(self, ctx: commands.Context, target: discord.Member, amount: int, give_rewards: int = 1):
        target_member = Member.get(target.id)
        await target_member.xp.set(amount, ctx, True if give_rewards == 1 else False)
        await ctx.reply(f"Set {target.mention} to `{amount} xp`")


async def setup(bot):
    await bot.add_cog(Levels(bot))
    print("Levels Cog loaded")


async def teardown(bot):
    print("Levels Cog unloaded")
    await bot.remove_cog(Levels(bot))
