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
            embed.description = f"<t:{int(datetime.utcnow().timestamp())}:D>"
            embed.colour = discord.Colour.dark_green()

            raid = SharkBot.Destiny.Raid.get_current()
            dungeon = SharkBot.Destiny.Raid.get_current()
            nightfall = SharkBot.Destiny.Nightfall.get_current()

            embed.add_field(
                name="Featured Raid",
                value=raid.name,
                inline=False
            )
            embed.add_field(
                name="Featured Dungeon",
                value=dungeon.name,
                inline=False
            )
            embed.add_field(
                name="This Week's Nightfall",
                value=f"{nightfall.name}\n{nightfall.gm_icons}",
                inline=False
            )

            await channel.send(embed=embed)

        embed = discord.Embed()
        embed.title = "Daily Reset!"
        embed.description = f"<t:{int(datetime.utcnow().timestamp())}:D>"
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
        description="Shows info about this season's GMs"
    )
    async def grandmaster(self, ctx: commands.Context) -> None:
        current = SharkBot.Destiny.Nightfall.get_current()

        embed = discord.Embed()
        embed.title = "Grandmaster Nightfalls"
        embed.description = f"Power Level Requirement: <:light_icon:1021555304183386203>1595"
        embed.colour = discord.Colour.dark_red()

        embed.add_field(
            name=f"{current.name} - {current.destination} (This Week)",
            value=current.gm_icons,
            inline=False
        )

        for nightfall in SharkBot.Destiny.Nightfall.rotation_from(current)[:5]:
            embed.add_field(
                name=f"{nightfall.name} - {nightfall.destination}",
                value=nightfall.gm_icons,
                inline=False
            )

        await ctx.reply(embed=embed, mention_author=False)

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

    @destiny.command(
        description="Gives the XP requirements for the given artifact power bonus."
    )
    async def bonus(self, ctx: commands.Context, level: int = 1):
        embed = discord.Embed()
        embed.title = "Artifact Power Bonus"
        embed.colour = discord.Colour.teal()
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/b1fe56d925a2ffc41d23e4c2ac5bdbb3.jpg"
        )

        def calc_xp(targetlevel: int) -> int:
            return ((targetlevel-2) * 110000) + 55000

        if level < 1:
            embed.description = "Power Bonus must be greater than zero, dangus"
        else:
            if level == 1:
                embed.description = "+1 given by default"
                bonusRange = list(range(2, 6))
            else:
                bonusRange = list(range(level, level+5))

            for lvl in bonusRange:
                xp = calc_xp(lvl)
                totalxp = sum([calc_xp(x) for x in range(2, lvl+1)])
                embed.add_field(
                    name=f"`+{'{:,}'.format(lvl)}` Bonus",
                    value=f"`{'{:,}'.format(xp)}` xp\n`{'{:,}'.format(totalxp)}` xp total",
                    inline=False
                )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Destiny(bot))
    print("Destiny Cog loaded")


async def teardown(bot):
    print("Destiny Cog unloaded")
    await bot.remove_cog(Destiny(bot))
