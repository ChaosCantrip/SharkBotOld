import discord
from datetime import datetime
from discord.ext import commands, tasks

import SharkBot


class Destiny(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reset.start()

    def cog_unload(self) -> None:
        self.reset.cancel()

    @tasks.loop(time=SharkBot.Destiny.resetTime)
    async def reset(self) -> None:
        sector = SharkBot.Destiny.LostSector.get_current()

        embed = discord.Embed()
        embed.title = "Daily Reset!"
        embed.description = f"<t:{int(datetime.now().timestamp())}:D>"
        embed.add_field(
            name="Today's Lost Sector",
            value=f"{sector.name} - {sector.destination}"
        )

        channel = await self.bot.fetch_channel(SharkBot.IDs.channels["SharkBot Commands"])
        await channel.send(embed=embed)

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

    @destiny.command(
        description="Gives a countdown to the release of Lightfall"
    )
    async def countdown(self, ctx: commands.Context) -> None:
        embed = discord.Embed()
        embed.title = "Lightfall Countdown"
        embed.description = SharkBot.Destiny.lightfallCountdown.time_remaining_string
        embed.description += "until Lightfall releases"
        embed.add_field(
            name="Release Date",
            value="28th February 2023 (Also Chaos' 21st Birthday!)"
        )

        await ctx.reply(embed=embed, mention_author=False)

    @destiny.command(
        description="Gives information about this week's raids."
    )
    async def raid(self, ctx: commands.Context) -> None:
        seasonal = SharkBot.Destiny.Raid.seasonal
        featured = SharkBot.Destiny.Raid.get_current()

        embed = discord.Embed()
        embed.title = "Raids"
        embed.add_field(
            name="Seasonal",
            value=seasonal.name,
            inline=False
        )
        embed.add_field(
            name="Featured",
            value=featured.name,
            inline=False
        )

        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot):
    await bot.add_cog(Destiny(bot))
    print("Destiny Cog loaded")


async def teardown(bot):
    print("Destiny Cog unloaded")
    await bot.remove_cog(Destiny(bot))
