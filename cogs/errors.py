import logging
import traceback
from typing import TypedDict, Optional, NotRequired

import discord
from discord.ext import commands

import SharkBot

cog_logger = logging.getLogger("cog")

class FieldDict(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]

async def send_error_embed(
        ctx: commands.Context, title: str, description: str, colour: discord.Colour = discord.Colour.red(),
        send_usage: bool = True, send_slash: bool = True, fields: Optional[list[FieldDict]] = None,
        mention_author: bool = False
) -> None:
    embed = discord.Embed(
        title=title,
        description=description,
        colour=colour
    )
    if ctx.command is not None and ctx.command.usage is not None and send_usage:
        embed.add_field(
            name="Command Usage",
            value=f"`{ctx.command.usage}`",
            inline=False
        )
    if isinstance(ctx.command, (commands.HybridCommand, commands.HybridGroup, discord.app_commands.AppCommand, discord.app_commands.AppCommandGroup)) and send_slash:
        embed.set_footer(
            text=f"This command is available as \"/{ctx.command.qualified_name}\", which will help with the arguments."
        )
    if fields is not None:
        for field_data in fields:
            embed.add_field(**field_data)

    await ctx.reply(embed=embed, mention_author=mention_author)


class Errors(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):

        # Error Conversion

        if isinstance(error, commands.errors.HybridCommandError):
            error = error.original

        if isinstance(error, commands.errors.ConversionError):
            if isinstance(error.original, SharkBot.Errors.SharkError):
                error = error.original

        if isinstance(error, (commands.CommandInvokeError, discord.app_commands.CommandInvokeError)):
            error = error.original

        # Basic

        if isinstance(error, commands.CommandNotFound):
            close_command = SharkBot.Utils.get_similar_commands(ctx.bot, ctx.message.content.split(" ")[0][1:])
            if close_command is None:
                await send_error_embed(
                    ctx=ctx,
                    title="Command Not Found!",
                    description=f"Sorry, I don't know that command!"
                )
            else:
                await send_error_embed(
                    ctx=ctx,
                    title="Command Not Found!",
                    description=f"Sorry, I don't know that command! Did you mean `${close_command}`?"
                )
            return

        if isinstance(error, commands.NoPrivateMessage):
            await send_error_embed(
                ctx=ctx,
                title="I have Anti-Social Anxiety...",
                description=f"I'm afraid that command can only be used inside a server!"
            )
            return

        # Permissions

        if isinstance(error, (commands.MissingRole, commands.MissingPermissions, commands.NotOwner)):
            await send_error_embed(
                ctx=ctx,
                title="Missing Permissions!",
                description=f"I'm afraid you don't have permission to do that!"
            )
            if isinstance(error, commands.NotOwner):
                owner = self.bot.get_user(self.bot.owner_id)
                if owner is None:
                    owner = await self.bot.fetch_user(self.bot.owner_id)
                await owner.send(f"{ctx.author.mention} tried to use {ctx.command} in {ctx.channel.mention}!")
            return

        if isinstance(error, (commands.CheckAnyFailure, commands.CheckFailure)):
            await send_error_embed(
                ctx=ctx,
                title="Command Check Failure!",
                description=f"I'm afriad you can't do that!"
            )
            return

        # Arguments

        if isinstance(error, commands.MissingRequiredArgument):
            await send_error_embed(
                ctx=ctx,
                title="Missing Argument!",
                description=f"I think you might be missing the `{error.param.name}` argument!"
            )
            return

        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Please enter a valid channel!")
            return

        if isinstance(error, commands.errors.BadArgument):
            await send_error_embed(
                ctx=ctx,
                title="Bad Argument!",
                description=f"I couldn't understand one of your arguments!",
                fields=[
                    {
                        "name": "__Error Message__",
                        "value": message
                    } for message in error.args
                ]
            )
            return

        if isinstance(error, commands.BadLiteralArgument):
            await send_error_embed(
                ctx=ctx,
                title="Invalid Argument!",
                description=f"I'm afraid I couldn't understand the argument for `{error.param.name}`!",
                fields=[
                    {
                        "name":"Possible Arguments",
                        "value":"\n".join(f"- `{literal}`" for literal in error.literals),
                        "inline":False
                    }
                ]
            )
            return

        # Admin

        if isinstance(error, commands.ExtensionNotLoaded):
            await send_error_embed(
                ctx=ctx,
                title="Extension Not Loaded!",
                description=f"I'm afraid the `{error.name}` Extension is not Loaded!"
            )
            return

        if isinstance(error, commands.ExtensionNotFound):
            await send_error_embed(
                ctx=ctx,
                title="Extension Not Found!",
                description=f"I'm afraid I couldn't find the `{error.name}` Extension!"
            )
            return

        # SharkErrors

        if isinstance(error, SharkBot.Errors.SharkError):
            if await error.handler(ctx):
                return

        # Unhandler Errors

        error_type = type(error)
        logging.error(f"{error_type.__module__}.{error_type.__name__}{error.args}")
        error_name = f"{error_type.__module__}.{error_type.__name__}"

        embed = discord.Embed()
        embed.title = "Something went wrong!"
        embed.colour = discord.Color.red()
        embed.description = "Oh no! An error occurred! I've let James know, and they'll do what they can to fix it!"
        embed.set_footer(text=error_name)
        await ctx.send(embed=embed)

        dev = await self.bot.fetch_user(SharkBot.IDs.dev)
        embed = discord.Embed()
        embed.title = "Error Report"
        embed.description = "Oopsie Woopsie"
        embed.add_field(name="Type", value=error_name, inline=False)
        embed.add_field(name="Args", value=error.args, inline=False)
        embed.add_field(name="Traceback", value="\n".join(traceback.format_tb(error.__traceback__)), inline=False)
        for e in SharkBot.Utils.split_embeds(embed):
            await dev.send(embed=e)

        raise error


async def setup(bot):
    await bot.add_cog(Errors(bot))
    print("Errors Cog Loaded")
    cog_logger.info("Errors Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Errors(bot))
    print("Errors Cog Unloaded")
    cog_logger.info("Errors Cog Unloaded")