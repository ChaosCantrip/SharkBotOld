import discord
from discord.ext import commands

import SharkBot

class Checks:

    @staticmethod
    def is_mod():
        async def predicate(ctx: commands.Context) -> bool:
            return ctx.author.id in SharkBot.IDs.mods
        return commands.check(predicate)