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

    @commands.hybrid_group()
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
                Rewards: {', '.join([item.text for item in mission.rewards])}\n"""
            embed.add_field(
                name=f"{missionType} Missions",
                value=outputText
            )

        await ctx.reply(embed=embed)

    @missions.command()
    async def claim(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Mission Rewards!"
        embed.set_thumbnail(url=ctx.author.avatar.url)

        completedMissions = [mission for mission in member.missions.missions if mission.completed]

        for mission in completedMissions:
            if mission.can_claim:
                embed.add_field(
                    name=mission.name,
                    value=f"""*{mission.description}*
                    You got {', '.join([item.text for item in mission.rewards])}!""",
                    inline=False
                )
                mission.claimed = True
                member.inventory.add(mission.rewards)
            else:
                embed.add_field(
                    name=mission.name,
                    value=f"*{mission.description}*\nAlready claimed!",
                    inline=False
                )

        await ctx.reply(embed=embed)
        member.write_data()


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog loaded")


async def teardown(bot):
    print("Missions Cog unloaded")
    await bot.remove_cog(Missions(bot))
