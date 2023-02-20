import discord
from discord.ext import commands

import SharkBot

class Checks:

    @staticmethod
    def is_mod():
        async def predicate(ctx: commands.Context) -> bool:
            result = ctx.author.id in SharkBot.IDs.mods
            if result is False:
                raise commands.MissingPermissions(["Mod"])
            return result
        return commands.check(predicate)