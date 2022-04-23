import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

	
	
class Admin(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
		
		
def setup(bot):
	bot.add_cog(Admin(bot))
	print("Admin Cog loaded")

def teardown(bot):
	print("Admin Cog unloaded")
	bot.remove_cog(Admin(bot))
