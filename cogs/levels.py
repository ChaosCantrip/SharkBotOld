import discord
from discord.ext import tasks, commands

from SharkBot import Member, IDs, XP


class Levels(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def level(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Level"
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.description = f"You are **Level {member.xp.level}** with `{member.xp.xp} xp`"

        embed.add_field(
            name=f"XP to Level {member.xp.level + 1}",
            value=f"`{member.xp.xp_to_next} xp` to go"
        )

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

    @commands.command()
    @commands.is_owner()
    async def initialise_xp(self, ctx: commands.Context):
        for member in Member.members.values():
            amount = 0
            amount += member.collection.xp_value
            amount += 3 * member.stats.completedMissions
            amount += member.counts
            await member.xp.set(amount, ctx)

        output = "\n".join(f"{member.id} | {member.xp.xp} | {member.xp.level}" for member in Member.members.values())

        await ctx.reply(output)

    @commands.hybrid_command()
    async def get_level(self, ctx: commands.Context, target: discord.Member):
        member = Member.get(target.id)

        embed = discord.Embed()
        embed.title = f"{target.display_name}'s Level"
        embed.set_thumbnail(url=target.avatar.url)
        embed.description = f"{target.mention} is **Level {member.xp.level}** with `{member.xp.xp} xp`"

        await ctx.reply(embed=embed)





async def setup(bot):
    await bot.add_cog(Levels(bot))
    print("Levels Cog loaded")


async def teardown(bot):
    print("Levels Cog unloaded")
    await bot.remove_cog(Levels(bot))
