import discord
from discord.ext import tasks, commands

import secret
from definitions import Member, Mission

if secret.testBot:
    import testids as ids
else:
    import ids


class Missions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def missions(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Missions"
        embed.set_thumbnail(url=ctx.author.avatar.url)

        for missionType in Mission.types:
            missions = [mission for mission in member.missions.missions if mission.type == missionType]
            outputText = ""
            for mission in missions:
                outputText += f"""\n**{mission.description}**
                Progress: {mission.progress}/{mission.quota} done
                Rewards: {mission.rewardsText}\n"""
            embed.add_field(
                name=f"{missionType} Missions",
                value=outputText
            )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog loaded")


async def teardown(bot):
    print("Missions Cog unloaded")
    await bot.remove_cog(Missions(bot))
