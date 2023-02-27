import json
from typing import Optional, Literal, Callable
import logging
import io

import discord
from datetime import datetime, date, time, timedelta
from discord.ext import commands, tasks

task_logger = logging.getLogger("task")

import SharkBot

_LOADING_ICON_URL = "https://cdn.dribbble.com/users/2081/screenshots/4645074/loading.gif"

with open("data/static/bungie/definitions/PatternSources.json", "r") as infile:
    _source_dict: dict[str, list[str]] = json.load(infile)
    _all_sources: list[str] = []
    for sources in _source_dict.values():
        _all_sources.extend(sources)
    _all_sources = list(set(_all_sources))

def get_source(search: str) -> list[str]:
    search = search.lower()
    if search in ["*", "all"]:
        return _all_sources
    source = _source_dict.get(search, None)
    if source is None:
        raise SharkBot.Errors.SourceNotFoundError(search.title())
    else:
        return source

SEAL_HASHES: dict[str, str] = {
    seal_name.lower(): seal_hash for seal_name, seal_hash in SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealHashes.json").items()
}

import logging

cog_logger = logging.getLogger("cog")

class Destiny(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.check_tokens.start()
        self.reset.start()
        self.check_manifest_loop.start()

    def cog_unload(self) -> None:
        self.reset.cancel()
        self.check_tokens.cancel()
        self.check_manifest_loop.cancel()

    @tasks.loop(time=time(hour=13))
    async def check_tokens(self):
        for member in SharkBot.Member.members:
            if member.bungie.refresh_token_expiring:
                await member.bungie.soft_refresh()
                dev = self.bot.get_user(SharkBot.IDs.dev)
                if dev is None:
                    dev = await self.bot.fetch_user(SharkBot.IDs.dev)
                await dev.send(f"Performed auto-token refresh for {member.id}")


    @tasks.loop(time=SharkBot.Destiny.reset_time)
    async def reset(self) -> None:
        channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Destiny Reset"])
        embeds = SharkBot.Destiny.Reset.get_embeds()
        for embed in embeds:
            task_logger.info(f"Sent '{embed.title}' Embed")
            await channel.send(embed=embed)

    @commands.hybrid_group()
    async def destiny(self, ctx: commands.Context) -> None:
        await ctx.send_help(self.destiny)

    @destiny.command()
    async def component_types(self, ctx: commands.Context, long_format: bool = False):
        embed = discord.Embed()
        embed.title = "ComponentTypeEnum"
        embed.description = "This is a list of ComponentTypeEnum within the Bungie API. If you don't know what that is, then it's not that important, just ignore it."
        if long_format:
            for component_type in SharkBot.Destiny.ComponentTypeEnum.enum_list:
                embed.add_field(
                    name=f"{component_type.name} - {component_type.enum}",
                    value=component_type.description,
                    inline=False
                )
        else:
            embed.description += "\n\n" + "\n".join(f"`{component_type.enum}` {component_type.name}" for component_type in SharkBot.Destiny.ComponentTypeEnum.enum_list)

        for e in SharkBot.Utils.split_embeds(embed):
            await ctx.reply(embed=e, mention_author=False)


    @destiny.command()
    @SharkBot.Checks.is_mod()
    async def send_embeds(self, ctx: commands.Context, channel: discord.TextChannel, include_weekly: bool = False):
        await ctx.send("Sending Destiny Reset Embeds")
        if channel.id == SharkBot.IDs.channels["Destiny Reset"]:
            await ctx.send("Deleting old embeds")
            async for message in channel.history(limit=10, after=(datetime.today() - timedelta(days=1))):
                if message.author.id != SharkBot.IDs.users["SharkBot"]:
                    continue
                await message.delete()
        embeds = SharkBot.Destiny.Reset.get_embeds(include_weekly)
        for embed in embeds:
            await channel.send(embed=embed)

    @destiny.command(
        description="Shows info about today's active Lost Sector"
    )
    async def sector(self, ctx: commands.Context) -> None:
        current_sector = SharkBot.Destiny.LostSector.get_current()
        reward = SharkBot.Destiny.LostSectorReward.get_current()

        if current_sector is None:
            embed = discord.Embed()
            embed.title = "Today's Lost Sector"
            embed.description = "Lost Sector Unknown (Season just started)"
            embed.set_thumbnail(
                url="https://www.bungie.net/common/destiny2_content/icons/6a2761d2475623125d896d1a424a91f9.png"
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed()
        embed.title = f"{current_sector.name}\n{current_sector.destination}"
        embed.description = f"{current_sector.burn} Burn {reward}"
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/6a2761d2475623125d896d1a424a91f9.png"
        )
        embed.add_field(
            name="Legend <:light_icon:1021555304183386203> 1580",
            value=f"{current_sector.legend.details}"
        )
        embed.add_field(
            name="Master <:light_icon:1021555304183386203> 1610",
            value=f"{current_sector.master.details}"
        )

        await ctx.send(embed=embed)

    @destiny.command(
        description="Shows info about today's Nightfall"
    )
    @discord.app_commands.choices(
        nightfall=[
            discord.app_commands.Choice(name=nf.name, value=nf.name) for nf in SharkBot.Destiny.Nightfall.nightfalls
        ]
    )
    async def nightfall(self, ctx: commands.Context, nightfall: str = SharkBot.Destiny.Nightfall.get_current().name):
        current_nightfall = SharkBot.Destiny.Nightfall.get(nightfall)

        if current_nightfall is None:
            embed = discord.Embed()
            embed.title = "This Week's Nightfall"
            embed.description = "Nightfall Rotation Unknown (Season just started)"
            embed.set_thumbnail(
                url="https://www.bungie.net/common/destiny2_content/icons/a72e5ce5c66e21f34a420271a30d7ec3.png"
            )
            await ctx.reply(embed=embed, mention_author=False)
            return

        embed = discord.Embed()
        embed.title = f"{current_nightfall.name}\n{current_nightfall.destination}"
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/a72e5ce5c66e21f34a420271a30d7ec3.png"
        )
        embed.add_field(
            name="Legend <:light_icon:1021555304183386203> 1580",
            value=f"{current_nightfall.legend.details}"
        )
        embed.add_field(
            name="Master <:light_icon:1021555304183386203> 1610",
            value=f"{current_nightfall.master.details}"
        )

        await ctx.send(embed=embed)

    @destiny.command(
        description="Shows info about this season's GMs"
    )
    async def grandmaster(self, ctx: commands.Context) -> None:
        current = SharkBot.Destiny.Nightfall.get_current()

        if datetime.utcnow() < date(2023, 1, 17):
            embed = discord.Embed()
            embed.title = "Grandmaster Nightfalls"
            embed.description = "Grandmaster Nightfalls release on January 17th, 2023"
            await ctx.reply(embed=embed, mention_author=False)
            return

        embed = discord.Embed()
        embed.title = "Grandmaster Nightfalls"
        embed.description = f"Power Level Requirement: <:light_icon:1021555304183386203>1605"
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
        for lostSector in SharkBot.Destiny.LostSector.lost_sectors:
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
        embed.description = SharkBot.Destiny.lightfall_countdown.time_remaining_string
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
    async def bonus(self, ctx: commands.Context, level: int):
        embed = discord.Embed()
        embed.title = "Artifact Power Bonus"
        embed.colour = discord.Colour.teal()
        embed.set_thumbnail(
            url="https://www.bungie.net/common/destiny2_content/icons/7b513c9215111507dbf31e3806cc1fcf.jpg"
        )

        def calc_xp(targetlevel: int) -> int:
            return ((targetlevel-2) * 110000) + 55000

        if level < 1:
            embed.description = "Power Bonus must be greater than zero, dangus"
        else:
            if level == 1:
                embed.description = "+1 given by default"
                bonus_range = list(range(2, 6))
            else:
                bonus_range = list(range(level, level+5))

            for lvl in bonus_range:
                xp = calc_xp(lvl)
                total_xp = sum([calc_xp(x) for x in range(2, lvl+1)])
                embed.add_field(
                    name=f"`+{'{:,}'.format(lvl)}` Bonus",
                    value=f"`{'{:,}'.format(xp)}` xp\n`{'{:,}'.format(total_xp)}` xp total",
                    inline=False
                )

        await ctx.send(embed=embed)

    @discord.app_commands.command(
        description="Authorizes SharkBot to get your Destiny 2 data from Bungie"
    )
    async def bungie_auth(self, interaction: discord.Interaction):
        embed = discord.Embed()
        embed.title = "Bungie Auth"
        embed.description = "In order to fetch your Destiny 2 Profile, you need to authorize SharkBot with Bungie\n"
        embed.description += "The link below will take you to the SharkBot OAuth2 portal, where you can sign in with your Bungie Account"
        embed.add_field(
            name="Bungie Auth Link",
            value=f"https://sharkbot.online/bungie_auth/discord/{interaction.user.id}"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @destiny.command(
        description="De-Authorizes SharkBot from your Bungie Account"
    )
    async def deauth(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        embed = discord.Embed()
        embed.title = "Bungie Deauthentication"
        embed.description = "Removing credentials from SharkBot..."
        embed.colour = discord.Colour.blurple()

        reply_message = await ctx.reply(embed=embed, mention_author=False)

        exists = member.bungie.delete_credentials()
        if exists:
            embed.description = "Removed Bungie Authentication."
            embed.colour = discord.Colour.green()
        else:
            embed.description = "Your Bungie Account is already not authorised with SharkBot"
            embed.colour = discord.Colour.red()

        await reply_message.edit(embed=embed)


    @destiny.command(
        description="Shows your Progress with your craftable weapons"
    )
    async def patterns(self, ctx: commands.Context, *, sources_search: str = "*"):
        sources_search = sources_search.split(", ")
        _sources: list[str] = []
        for search in sources_search:
            _sources.extend(get_source(search))

        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.craftables.send_embeds(ctx, _sources=_sources)

    @destiny.command(
        description="Shows your progress on the Conqueror Seal this season"
    )
    async def conqueror(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.conqueror.send_embeds(ctx)


    @destiny.command(
        description="Shows the weapons you are yet to acquire from the Monument to Lost Light"
    )
    async def monument(self, ctx: commands.Context, *, year: str = "*"):
        year = year.lower()
        if year == "*":
            years = ["1", "2", "3", "4", "5"]
        elif year in ["1", "one", "rw", "red war"]:
            years = ["1"]
        elif year in ["2", "two", "forsaken"]:
            years = ["2"]
        elif year in ["3", "three", "shadowkeep"]:
            years = ["3"]
        elif year in ["4", "four", "beyond", "beyond light"]:
            years = ["4"]
        elif year in ["5", "five", "wq", "witch queen"]:
            years = ["5"]
        else:
            await ctx.reply(f"`{year}` is not a valid Year for me to look for!")
            return

        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.monument.send_embeds(ctx, years=years)

    @destiny.command(
        description="Shows the levels of the weapons you have crafted"
    )
    async def levels(self, ctx: commands.Context, filter_by: Optional[Literal["<", "<=", "=", ">=", ">"]] = None, level: Optional[int] = None):

        f: Optional[Callable[[list[str, int, str]], bool]] = None
        if filter_by is not None:
            if level is None:
                embed = discord.Embed()
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
                embed.colour = discord.Colour.red()
                embed.title = "Something went wrong!"
                embed.description = "You can't specify a filter and then no value to filter off of!"
                await ctx.reply(embed=embed)
                return
            else:
                if filter_by == "<":
                    f = lambda d: d[1] < level
                elif filter_by == "<=":
                    f = lambda d: d[1] <= level
                elif filter_by == "=":
                    f = lambda d: d[1] == level
                elif filter_by == ">=":
                    f = lambda d: d[1] >= level
                elif filter_by == ">":
                    f = lambda d: d[1] > level
                else:
                    embed = discord.Embed()
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
                    embed.colour = discord.Colour.red()
                    embed.title = "Something went wrong!"
                    embed.description = f"I don't recognise `{filter_by}` as a filter condition. Please use `<`, `<=`, `=`, `>=` or `>`"
                    await ctx.reply(embed=embed)
                    return

        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.weapon_levels.send_embeds(ctx, f=f)

    @destiny.command()
    async def currencies(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.currencies.send_embeds(ctx)

    @destiny.command()
    async def prep(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.bounty_prep.send_embeds(ctx)

    @destiny.command()
    async def seal(self, ctx: commands.Context, *, seal: str):
        if seal not in SEAL_HASHES.values():
            if seal.lower() in SEAL_HASHES:
                seal = SEAL_HASHES[seal.lower()]
            else:
                raise SharkBot.Destiny.Errors.SealNotFoundError(seal)
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        await member.bungie.seals.send_embeds(ctx, seal_hash=seal)

    @seal.autocomplete("seal")
    async def seal_seal_autocomplete(self, interaction: discord.Interaction, current: str):
        return await SharkBot.Autocomplete.seal(interaction, current)

    @destiny.command()
    async def wellspring(self, ctx: commands.Context):
        current_wellspring = SharkBot.Destiny.Wellspring.get_current()
        embed = discord.Embed(
            title=f"Wellspring: __{current_wellspring.mode}__"
        )
        embed.add_field(
            name="Weapon",
            value=f"{current_wellspring.weapon.icons} **{current_wellspring.weapon.name}**\n*{current_wellspring.weapon.type}*",
            inline=False
        )
        embed.add_field(
            name="Boss",
            value=f"*{current_wellspring.boss}*",
            inline=False
        )
        embed.set_thumbnail(url="https://www.light.gg/Content/Images/wellspring-icon.png")
        embed.colour = discord.Colour.dark_green()
        await ctx.reply(embed=embed, mention_author=False)

    @destiny.command()
    @commands.is_owner()
    async def check_manifest_version(self, ctx: commands.Context):
        message = await ctx.reply(f"Checking Manifest Version against `{SharkBot.Destiny.Manifest.MANIFEST_VERSION}`")
        if await SharkBot.Destiny.Manifest.is_outdated():
            await message.edit(content=f"Manifest `{SharkBot.Destiny.Manifest.MANIFEST_VERSION}` out of date.")
        else:
            await message.edit(content=f"Manifest `{SharkBot.Destiny.Manifest.MANIFEST_VERSION}` up to date.")

    @tasks.loop(hours=4)
    async def check_manifest_loop(self):
        task_logger.info("Checking Destiny Manifest Version")
        if await SharkBot.Destiny.Manifest.is_outdated():
            task_logger.warning("Destiny Manifest Outdated")
            dev = await self.bot.fetch_user(SharkBot.IDs.dev)
            await dev.send("New Destiny Manifest Version Available")
        else:
            task_logger.info("Checking Destiny Manifest Up to Date")

    @check_manifest_loop.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Destiny(bot))
    print("Destiny Cog Loaded")
    cog_logger.info("Destiny Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Destiny(bot))
    print("Destiny Cog Unloaded")
    cog_logger.info("Destiny Cog Unloaded")