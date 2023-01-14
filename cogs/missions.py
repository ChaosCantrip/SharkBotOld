import discord
from discord.ext import commands

import SharkBot.Utils
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
            spacer = "" if missionType == "Daily" else "______\n\n"
            embed.add_field(
                name=spacer + missionType + " Missions",
                value=f"*Can be completed {missionType}*",
                inline=False
            )
            missions = [mission for mission in member.missions.missions if mission.type == missionType]
            for mission in missions:
                embed.add_field(
                    name=mission.description,
                    value=f"Progress: {mission.progress}/{mission.quota} done\n{mission.rewards_text}\n",
                    inline=False
                )

        for e in SharkBot.Utils.split_embeds(embed, "\n\n"):
            await ctx.reply(embed=e, mention_author=False)


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog loaded")


async def teardown(bot):
    print("Missions Cog unloaded")
    await bot.remove_cog(Missions(bot))
