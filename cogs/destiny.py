import discord
from discord.ext import commands

import SharkBot


class Destiny(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group()
    async def destiny(self, ctx: commands.Context) -> None:
        await ctx.send("Destiny Command")

    @destiny.command(
        description="Shows info about today's active Lost Sector"
    )
    async def sector(self, ctx: commands.Context) -> None:
        currentSector = SharkBot.Destiny.LostSector.get_current()
        reward = SharkBot.Destiny.LostSectorReward.get_current()

        embed = discord.Embed()
        embed.title = f"{currentSector.name}\n{currentSector.destination}"
        embed.description = f"{currentSector.burn.text} Burn {reward.text}"
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/6a2761d2475623125d896d1a424a91f9.png"
        )
        embed.add_field(
            name="Legend <:light_icon:1021555304183386203> 1570",
            value=f"{currentSector.legend.details}"
        )
        embed.add_field(
            name="Master <:light_icon:1021555304183386203> 1600",
            value=f"{currentSector.master.details}"
        )

        await ctx.send(embed=embed)

    @destiny.command(
        hidden=True
    )
    async def sector_list(self, ctx: commands.Context) -> None:
        embed = discord.Embed()
        embed.title = "Lost Sectors"
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/6a2761d2475623125d896d1a424a91f9.png"
        )
        for lostSector in SharkBot.Destiny.LostSector.lostSectors:
            embed.add_field(
                name=f"{lostSector.name} - {lostSector.destination}",
                value=f"Champions: *{lostSector.champion_list}*\nShields: *{lostSector.shield_list}*",
                inline=False
            )

        await ctx.send(embed=embed)

    @destiny.command(
        description="Gives details about the current Season"
    )
    async def season(self, ctx: commands.Context) -> None:
        season = SharkBot.Destiny.Season.current
        embed = discord.Embed()
        embed.title = f"Season {season.number} - {season.name}"
        embed.description = f"**{season.calendar_string}**\n{season.time_remaining_string} left in the Season"
        embed.set_thumbnail(
            url=season.icon
        )

        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot):
    await bot.add_cog(Destiny(bot))
    print("Destiny Cog loaded")


async def teardown(bot):
    print("Destiny Cog unloaded")
    await bot.remove_cog(Destiny(bot))
