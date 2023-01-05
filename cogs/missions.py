import discord
from discord.ext import commands

from SharkBot import Member, Mission


class Missions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["m"])
    async def missions(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Missions"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        for missionType in Mission.Mission.types:
            missions = [mission for mission in member.missions.missions if mission.type == missionType]
            output_text = ""
            for mission in missions:
                output_text += f"""\n**{mission.description}**
                Progress: {mission.progress}/{mission.quota} done
                Rewards: {mission.rewards_text}\n"""
            embed.add_field(
                name=f"{missionType} Missions",
                value=output_text
            )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog loaded")


async def teardown(bot):
    print("Missions Cog unloaded")
    await bot.remove_cog(Missions(bot))
