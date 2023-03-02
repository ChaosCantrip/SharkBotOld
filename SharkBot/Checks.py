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
            if ctx.guild is None:
                dev = ctx.bot.get_user(SharkBot.IDs.dev)
                if dev is None:
                    dev = await ctx.bot.fetch_user(SharkBot.IDs.dev)
                await dev.send(SharkBot.Utils.command_usage(ctx))
            return result
        return commands.check(predicate)

    @staticmethod
    def disabled(message: str = "This command has temporarily been disabled."):
        async def predicate(ctx: commands.Context) -> bool:
            raise SharkBot.Errors.CommandDisabledError(message)
        return commands.check(predicate)