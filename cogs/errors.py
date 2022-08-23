import discord
import mysql.connector.errors
from discord.ext import tasks, commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I don't know that command!")
            return
        if isinstance(error, commands.CheckAnyFailure):
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
        if isinstance(error, mysql.connector.errors.DatabaseError):
            chaos = await self.bot.fetch_user(ids.users["Chaos"])
            await chaos.send("Couldn't connect to SIMP database.")
            await chaos.send(error.name + " " + error.args)
            return
        if isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm afraid you don't have permission to do that!")
            return

        errorType = type(error)
        errorName = f"{errorType.__module__}.{errorType.__name__}{error.args}"

        embed = discord.Embed()
        embed.title = "Something went wrong!"
        embed.color = discord.Color.red()
        embed.description = "Oh no! An error occurred! I've let James know, and they'll do what they can to fix it!"
        embed.set_footer(text=errorName)
        await ctx.send(embed=embed)

        chaos = await self.bot.fetch_user(ids.users["Chaos"])
        embed = discord.Embed()
        embed.title = "Error Report"
        embed.description = "Oopsie Woopsie"
        embed.add_field(name="Type", value=errorName, inline=False)
        embed.add_field(name="Args", value=error.args, inline=False)
        await chaos.send(embed=embed)

        raise error


async def setup(bot):
    await bot.add_cog(Errors(bot))
    print("Errors Cog loaded")


async def teardown(bot):
    print("Errors Cog unloaded")
    await bot.remove_cog(Errors(bot))
