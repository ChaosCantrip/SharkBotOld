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
