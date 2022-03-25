import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

	
	
class Purchases(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
		
		
def setup(bot):
	bot.add_cog(Purchases(bot))
	print("Purchases Cog loaded")

def teardown(bot):
	print("Purchases Cog unloaded")
	bot.remove_cog(Purchases(bot))
