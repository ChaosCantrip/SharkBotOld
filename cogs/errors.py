import logging
import traceback

import discord
from discord.ext import commands

import SharkBot

cog_logger = logging.getLogger("cog")

class Errors(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.HybridCommandError):
            error = error.original
        if isinstance(error, commands.errors.ConversionError):
            if isinstance(error.original, SharkBot.Errors.SharkError):
                error = error.original
        if isinstance(error, commands.CommandInvokeError) or isinstance(error, discord.app_commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I don't know that command!")
            return
        if isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm afraid you don't have permission to do that!")
            return
        if isinstance(error, commands.NotOwner):
            owner = self.bot.get_user(self.bot.owner_id)
            if owner is None:
                owner = await self.bot.fetch_user(self.bot.owner_id)
            await ctx.reply(f"Sorry, only {owner.mention} can do that!")
            await owner.send(f"{ctx.author.mention} tried to use {ctx.command} in {ctx.channel.mention}!")
            return
        if isinstance(error, (commands.CheckAnyFailure, commands.CheckFailure)):
            await ctx.send("Sorry, you can't do that!")
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("I think you're missing an argument there!")
            return
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Please enter a valid channel!")
            return
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("Please enter a valid argument!")
            return
        if isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send("Extension not loaded!")
            return
        if isinstance(error, commands.ExtensionNotFound):
            await ctx.send("Extension not found!")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can only be used inside a server!")
            return
        if isinstance(error, commands.BadLiteralArgument):
            embed = discord.Embed()
            embed.title = "Invalid Argument!"
            embed.colour = discord.Colour.red()
            embed.description = f"I'm afraid I couldn't understand the argument for `<{error.param.name}>`!"
            if ctx.command.usage is not None:
                embed.add_field(
                    name="Command Usage",
                    value=f"`{ctx.command.usage}`",
                    inline=False
                )
            embed.add_field(
                name="Possible Arguments",
                value="\n".join(f"- `{literal}`" for literal in error.literals),
                inline=False
            )
            if isinstance(ctx.command, (commands.HybridCommand, commands.HybridGroup, discord.app_commands.AppCommand, discord.app_commands.AppCommandGroup)):
                embed.set_footer(
                    text="This command is available as a slash command, which will help show the available options."
                )
            await ctx.reply(embed=embed, mention_author=False)
            return

        if isinstance(error, SharkBot.Errors.SharkError):
            if await error.handler(ctx):
                return

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