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
		
	def name_comm(userName, textName):
		await ctx.send("Command not found. Try $v to get started.")
      		
	
	def show_comm(userName, mapName):
		await ctx.send("Command not found. Try $v to get started.")
      		
		
	def update_comm(userName, mapName, agentList):
		await ctx.send("Command not found. Try $v to get started.")
      		
		
	def add_comm(userName, mapName, agentList):
		await ctx.send("Command not found. Try $v to get started.")
      		
		
	def remove_comm(userName, mapName, agentList):
		await ctx.send("Command not found. Try $v to get started.")
      		
	
	def new_comm(mapName, user1, user2, user3, user4, user5):
		await ctx.send("Command not found. Try $v to get started.")
      		
	
	def lock_comm(userName, agentName):
		await ctx.send("Command not found. Try $v to get started.")
      		
    
	@commands.command(name="valorant", aliases=["val", "v"], brief="Default Valorant command.")
	async def val_comm(self, ctx, comm, arg1, arg2, arg3, arg4, arg5, arg6):
  	if comm == "name":
    		name_comm(arg1, arg2)
	elif comm == "show" or comm == "s"  or comm == "agents" or comm == "agent" or comm == "a":
		show_comm(arg1, arg2)
    	elif comm == "update" or comm == "u" or comm == "replace" or comm == "rep":
      		update_comm(arg1, arg2, arg3)
    	elif comm == "add":
      		add_comm(arg1, arg2, arg3)
    	elif comm == "remove" or comm == "rem":
      		remove_comm(arg1, arg2, arg3)
    	elif comm == "new" or comm == "n" or comm == "game" or comm == "g" or comm == comm == "map" or comm == "m":
      		new_comm(arg1, arg2, arg3, arg4, arg5, arg6)
    	elif comm == "locked" or comm == "lock" or comm == "l" or comm == "picked" or comm == "picks" or comm == "pick" or comm == "p":
      		lock_comm(arg1, arg2)
    	else:
		helpEmbed = discord.Embed(title="Valorant Commands", color=0x660000)
		commList = ""
		commList = commList + f"$v name <user> <name> - Sets the user's text name for use in commands and display. \n"
		commList = commList + f"$v show <user> <map> - Shows the user's agent list for this map. \n"
		commList = commList + f"$v update <user> <map> <agent list> - Replaces the user's list of played agents for this map. \n"
		commList = commList + f"$v add <user> <map> <agent list> - Adds the list of agents to the user's played agents for this map. \n"
		commList = commList + f"$v remove <user> <map> <agent list> - Removes the list of agents from the user's played agents for this map. \n"
		commList = commList + f"$v new <map> <user1> <user2> <user3> <user4> <user5> - Replaces map session with a new one and gives initial insight. \n"
		commList = commList + f"$v lock <user> <agent> - Updates current map session information using newly locked in agent. \n"
		helpEmbed.add_field(name="Command List", value=commList, inline=False)
      		await ctx.send(embed=helpEmbed)
		
		
		
def setup(bot):
	bot.add_cog(Valorant(bot))
	print("Valorant Cog loaded")

def teardown(bot):
	print("Valorant Cog unloaded")
	bot.remove_cog(Valorant(bot))
