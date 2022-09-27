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
        channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Destiny Reset"])
        weeklyReset = datetime.today().weekday() == 1

        if weeklyReset:
            embed = discord.Embed()
            embed.title = "Weekly Reset!"
            embed.colour = discord.Colour.dark_green()

            embed.add_field(
                name="Featured Raid",
                value=SharkBot.Destiny.Raid.get_current().name,
                inline=False
            )
            embed.add_field(
                name="Featured Dungeon",
                value=SharkBot.Destiny.Dungeon.get_current().name,
                inline=False
            )
            embed.add_field(
                name="This Week's Nightfall",
                value=SharkBot.Destiny.Nightfall.get_current().name,
                inline=False
            )

            await channel.send(embed=embed)

        embed = discord.Embed()
        embed.title = "Daily Reset!"
        embed.colour = discord.Colour.dark_gold()

        sector = SharkBot.Destiny.LostSector.get_current()
        sectorText = f"{sector.name} - {sector.destination}"
        sectorText += f"\n{sector.champion_list}, {sector.shield_list}"
        sectorText += f"\n{sector.burn.text} Burn, {SharkBot.Destiny.LostSectorReward.get_current().text}"

        embed.add_field(
            name="Today's Lost Sector",
            value=sectorText,
            inline=False
        )

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
        description="Shows info about today's Nightfall"
    )
    async def nightfall(self, ctx: commands.Context) -> None:
        currentNightfall = SharkBot.Destiny.Nightfall.get_current()

        embed = discord.Embed()
        embed.title = f"{currentNightfall.name}\n{currentNightfall.destination}"
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/a72e5ce5c66e21f34a420271a30d7ec3.png"
        )
        embed.add_field(
            name="Legend <:light_icon:1021555304183386203> 1570",
            value=f"{currentNightfall.legend.details}"
        )
        embed.add_field(
            name="Master <:light_icon:1021555304183386203> 1600",
            value=f"{currentNightfall.master.details}"
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
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/9230cd18bcb0dd87d47a554afb5edea8.png"
        )
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

    @destiny.command(
        description="Gives information about this week's dungeons."
    )
    async def dungeon(self, ctx: commands.Context) -> None:
        seasonal = SharkBot.Destiny.Dungeon.seasonal
        featured = SharkBot.Destiny.Dungeon.get_current()

        embed = discord.Embed()
        embed.title = "Dungeons"
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/082c3d5e7a44343114b5d056c3006e4b.png"
        )
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
