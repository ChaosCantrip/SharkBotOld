import discord
from discord.ext import commands

import SharkBot


import logging

cog_logger = logging.getLogger("cog")

class Missions(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["m"])
    async def missions(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Missions"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        for missionType in SharkBot.Mission.Mission.types:
            spacer = "" if missionType == "Daily" else "______\n\n"
            embed.add_field(
                name=spacer + missionType + " Missions",
                value=f"*Can be completed {missionType}*",
                inline=False
            )
            missions = [mission for mission in member.missions.missions if mission.type == missionType]
            for mission in missions:
                embed.add_field(
                    name=f"{mission.description} ({mission.progress}/{mission.quota})",
                    value=f"{mission.rewards_text}",
                    inline=False
                )

        for e in SharkBot.Utils.split_embeds(embed, "\n\n"):
            await ctx.reply(embed=e, mention_author=False)


async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions Cog Loaded")
    cog_logger.info("Missions Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Missions(bot))
    print("Missions Cog Unloaded")
    cog_logger.info("Missions Cog Unloaded")