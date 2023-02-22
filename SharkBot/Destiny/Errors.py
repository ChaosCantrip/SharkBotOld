import discord

from SharkBot.Errors import SharkError
from discord.ext import commands


class ChampionNotFoundError(SharkError):
    pass


class ShieldNotFoundError(SharkError):
    pass


class LostSectorNotFoundError(SharkError):
    pass


class LostSectorRewardNotFoundError(SharkError):
    pass


class DungeonNotFoundError(SharkError):
    pass


class RaidNotFoundError(SharkError):
    pass


class NightfallNotFoundError(SharkError):

    async def handler(self, ctx: commands.Context):
        await ctx.send("I couldn't find that Nightfall!")
        return True

class ComponentTypeEnumNotFoundError(SharkError):
    pass


class SealNotFoundError(SharkError):

    def __init__(self, seal: str):
        self.seal = seal

    async def handler(self, ctx: commands.Context) -> bool:
        embed = discord.Embed(
            title="Seal Not Found",
            description=f"I'm afraid I couldn't find `{self.seal}`! I'd reccommend using the slash command for this one, makes it easier for all of us <3",
            colour=discord.Colour.red()
        )
        await ctx.reply(embed=embed, mention_author=False)
        return True