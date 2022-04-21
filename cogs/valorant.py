import json
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
		 		
	
	def load_file(fileName, canCreate):
		try:
			with open(f"data/valorant/{fileName}.json", "r") as infile:
				return json.load(infile)
		except FileNotFoundError:
			if canCreate == True:
				createFile = open(f"data/valorant/{fileName}.json", "w")
				createFile.close()
			return {}
		
	async def save_file(data):
		with open("data/valorant/userdata.json", "w") as outfile:
			json.dump(data, outfile, indent=4)
		await ctx.send("List has been updated.")
		
	def check_file(target: discord.Member, mapName):
		data = load_file("userdata", True)
		key = f"{str(target)}, {mapName}"
		return data, key
	

	
	async def show_comm(target: discord.Member, mapName):
		data, key = check_file(target, mapName)
		if key in data:
			await ctx.send(data[key])
		else:
			await ctx.send("User has no agents registered for this map. Try adding them with $v add <user> <map> <agents>")
      		
		
	def update_comm(target: discord.Member, mapName, agentList):
		data, key = check_file(target, mapName)
		data[key] = agentList
		save_file(data)
		
      		
		
	def add_comm(target: discord.Member, mapName, agentList):
		data, key = check_file(target, mapName)
		for item in agentList:
			if item not in data[key]:
				data[key].append(item)
		save_file(data)
		
      		
		
	def remove_comm(target: discord.Member, mapName, agentList):
		data, key = check_file(target, mapName)
		for item in agentList:
			if item in data[key]:
				data[key].remove(item)
		save_file(data)
      		
	
	async def new_comm(mapName, target1: discord.Member, target2: discord.Member, target3: discord.Member, target4: discord.Member, target5: discord.Member):
		mapData = load_file(f"{mapName}data", False)
		if target1 == None:
			party = 0				 
		elif target2 == None:
			party = 1				 
		elif target3 == None:
			party = 2
		elif target4 == None:
			party = 3
		elif target5 == None:
			party = 4
		else:
			party = 5
							 
		if party != 0:
			ctx.send("Cheese!")
			
		
      		
	
	async def lock_comm(target: discord.Member, agentName):
		await ctx.send("Command not found. Try $v to get started.")
      		
    
	@commands.command(name="valorant", aliases=["val", "v"], brief="Default Valorant command.")
	async def val_comm(self, ctx, comm, arg1, arg2, arg3, arg4, arg5, arg6):
		if comm in ["show", "s", "agents", "agent", "a"]:
			show_comm(arg1, arg2)
    		elif comm in ["update", "u", "replace", "rep"]:
      			update_comm(arg1, arg2, arg3)
    		elif comm == "add":
      			add_comm(arg1, arg2, arg3)
    		elif comm in ["remove", "rem"]:
      			remove_comm(arg1, arg2, arg3)
    		elif comm in ["new", "n", "game", "g", "map", "m"]:
      			new_comm(arg1, arg2, arg3, arg4, arg5, arg6)
    		elif comm in ["locked", "lock", "l", "picked", "picks", "pick", "p"]:
      			lock_comm(arg1, arg2)
    		else:
			helpEmbed = discord.Embed(title="Valorant Commands", color=0x660000)
			commList = ""
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
