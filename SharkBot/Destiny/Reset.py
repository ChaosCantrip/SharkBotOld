import discord
from SharkBot import Destiny
from datetime import datetime


def weekly_embed() -> discord.Embed:
    embed = discord.Embed()
    embed.title = "Weekly Reset!"
    embed.description = f"<t:{int(Destiny.get_last_reset().timestamp())}:D>"
    embed.colour = discord.Colour.dark_green()

    current_raid = Destiny.Raid.get_current()
    embed.add_field(
        name="Featured Raid",
        value=current_raid.name,
        inline=False
    )

    current_dungeon = Destiny.Dungeon.get_current()
    embed.add_field(
        name="Featured Dungeon",
        value=current_dungeon.name,
        inline=False
    )

    current_nightfall = Destiny.Nightfall.get_current()
    if current_nightfall is None:
        nightfall_text = "Nightfall Rotation Unknown (Season just started)"
    else:
        nightfall_text = f"{current_nightfall.name}\n{current_nightfall.gm_icons}"

    embed.add_field(
        name="This Week's Nightfall",
        value=nightfall_text,
        inline=False
    )

    return embed


def daily_embed() -> discord.Embed:
    embed = discord.Embed()
    embed.title = "Daily Reset!"
    embed.description = f"<t:{int(Destiny.get_last_reset().timestamp())}:D>"
    embed.colour = discord.Colour.dark_gold()

    sector = Destiny.LostSector.get_current()
    if sector is not None:
        sector_text = f"{sector.name} - {sector.destination}"
        sector_text += f"\n{sector.champion_list}, {sector.shield_list}"
        sector_text += f"\n{sector.burn} Burn, {Destiny.LostSectorReward.get_current()}"
    else:
        sector_text = "Lost Sector Unknown (Season just started)"

    embed.add_field(
        name="Today's Lost Sector",
        value=sector_text,
        inline=False
    )

    return embed


def get_embeds(include_weekly: bool = False) -> list[discord.Embed]:
    output = []
    if include_weekly or Destiny.is_weekly_reset():
        output.append(weekly_embed())

    output.append(daily_embed())

    return output
