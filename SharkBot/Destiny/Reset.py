import discord
from SharkBot import Destiny
from datetime import datetime


def weekly_embed() -> discord.Embed:
    embed = discord.Embed()
    embed.title = "Weekly Reset!"
    embed.description = f"<t:{int(datetime.utcnow().timestamp())}:D>"
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
