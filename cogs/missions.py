import discord
from discord.ext import tasks, commands

import secret
from definitions import Member

if secret.testBot:
    import testids as ids
else:
    import ids


class Missions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group()
    async def missions(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Missions"
        embed.set_thumbnail(url=ctx.author.avatar.url)

        for mission in member.missions.missions:
            embed.add_field(
                name=f"{mission.mission.name} -> {mission.mission.reward.rarity.icon} *{mission.mission.reward.name}*",
                value=f"*{mission.mission.description}*\n{mission.progress}/{mission.mission.quota} done",
                inline=False
            )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog loaded")


async def teardown(bot):
    print("Missions Cog unloaded")
    await bot.remove_cog(Missions(bot))
