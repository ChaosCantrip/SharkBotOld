import discord
from discord.ext import commands

from SharkBot import Item


class XP:

    def __init__(self, xp: int, member):
        self.xp = xp
        self.level = xp_to_level(xp)
        self.member = member

    async def add(self, amount: int, ctx: commands.Context):
        self.xp += amount
        if xp_to_level(self.xp) > self.level:
            for level in range(self.level + 1, xp_to_level(self.xp) + 1):
                self.level = level
                rewards = get_level_rewards(self.level)

                embed = discord.Embed()
                embed.title = f"{ctx.author.display_name} Leveled Up!"
                embed.set_thumbnail(url=ctx.author.display_avatar.url)
                embed.description = f"You reached **Level {self.level}**!"
                embed.add_field(
                    name="Rewards",
                    value="\n".join([str(item) for item in rewards])
                )
                embed.set_footer(
                    text=f"XP: {self.xp}"
                )

                await ctx.reply(embed=embed)


xp_track = {
    0: 1,
    10: 2,
    25: 3,
    45: 4,
    70: 5,
    100: 6,
    140: 7,
    190: 8,
    250: 9,
    320: 10,
    400: 11,
    490: 12
}

max_xp_in_track = max(xp_track)


def xp_to_level(xp: int) -> int:
    if xp > max_xp_in_track:
        return 12 + int((xp - max_xp_in_track) / 100)
    else:
        for x, l in xp_track.items():
            if xp < x:
                return l - 1


def get_level_rewards(level: int) -> list[Item.Item]:
    output = [Item.get("LOOTSHARK")]
    if level % 10 == 0:
        output += [Item.get("LOOTSHARK"), Item.get("LOOTSHARK")]
    if level % 100 == 0:
        output += [Item.get("LOOTM")]

    return output
