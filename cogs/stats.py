import discord
from discord.ext import commands

import SharkBot


import logging

cog_logger = logging.getLogger("cog")

class Stats(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def stats(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        embed = discord.Embed()
        embed.title = "Your Stats"
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f"Counts: `{member.counts:,}`"
        embed.description += f"\nIncorrect Counts: `{member.stats.incorrect_counts:,}`"
        embed.description += f"\nCoinflips: `{member.stats.coinflips.num:,}`"
        embed.description += f"\nCoinflip KDA: `{member.stats.coinflips.kda}`"
        embed.description += f"\nCoinflip Win Rate: `{member.stats.coinflips.winrate}%`"
        embed.description += f"\nClaimed Boxes: `{member.stats.boxes.claimed:,}`"
        embed.description += f"\nBought Boxes: `{member.stats.boxes.bought:,}`"
        embed.description += f"\nOpened Boxes: `{member.stats.boxes.opened:,}`"
        embed.description += f"\nBoxes from Counting: `{member.stats.boxes.counting:,}`"
        embed.description += f"\nSold Items: `{member.stats.sold_items:,}`"
        embed.description += f"\nItem Collected: `{len(member.collection):,}`"
        embed.description += f"\nMissions Completed: `{member.stats.completed_missions:,}`"
        embed.set_footer(text="Stats began tracking on 04/09/2022")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot))
    print("Stats Cog Loaded")
    cog_logger.info("Stats Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Stats(bot))
    print("Stats Cog Unloaded")
    cog_logger.info("Stats Cog Unloaded")