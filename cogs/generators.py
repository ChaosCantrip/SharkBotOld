import discord
from discord.ext import commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

	
	
class Generators(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
		
		
def setup(bot):
	bot.add_cog(Generators(bot))
	print("Generators Cog loaded")

def teardown(bot):
	print("Generators Cog unloaded")
	bot.remove_cog(Generators(bot))
