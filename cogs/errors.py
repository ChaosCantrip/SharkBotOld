import discord
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
        
        chaos = await self.bot.fetch_user(ids.users["Chaos"])    
        embed = discord.Embed()
        embed.title = "Error Report"
        embed.description = "Oopsie Woopsie"
        embed.add_field(name="Type", value=type(error), inline=False)
        embed.add_field(name="Args", value=error.args, inline=False)
        await chaos.send(embed=embed)

        await ctx.send("Sorry, something went wrong!")

        raise error



def setup(bot):
	bot.add_cog(Errors(bot))
	print("Errors Cog loaded")

def teardown(bot):
	print("Errors Cog unloaded")
	bot.remove_cog(Errors(bot))
