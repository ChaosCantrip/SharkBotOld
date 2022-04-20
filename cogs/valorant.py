import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

	
	
class Valorant(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
    
  @commands.command(name="valorant", aliases=["val", "v"], brief="Default Valorant command.")
  async def val_comm(self, ctx, comm, arg1, arg2, arg3, arg4, arg5, arg6):
    if comm == "name":
      await ctx.send("Command not found. Try $v to get started.")
      return
    elif comm == "update" or comm == "u" or comm == "replace" or comm == "rep":
      await ctx.send("Command not found. Try $v to get started.")
      return
    elif comm == "add" or comm == "agents" or comm == "agent" or comm == "a":
      await ctx.send("Command not found. Try $v to get started.")
      return
    elif comm == "remove" or comm == "rem":
      await ctx.send("Command not found. Try $v to get started.")
      return
    elif comm == "new" or comm == "n" or comm == "game" or comm == "g" or comm == comm == "map" or comm == "m":
      await ctx.send("Command not found. Try $v to get started.")
      return
    elif comm == "locked" or comm == "lock" or comm == "l" or comm == "picked" or comm == "picks" or comm == "pick" or comm == "p":
      await ctx.send("Command not found. Try $v to get started.")
      return
    else:
      await ctx.send("Command not found. Try $v to get started.")
      return
		
		
		
def setup(bot):
	bot.add_cog(Valorant(bot))
	print("Valorant Cog loaded")

def teardown(bot):
	print("Valorant Cog unloaded")
	bot.remove_cog(Valorant(bot))
