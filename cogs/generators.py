import discord
from discord.ext import commands
from random import randint

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

	
	
class Generators(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def coinflip(self, ctx, flips = 1):

		results = {1:"Heads",2:"Tails"}
		if flips == 1:
			await ctx.send(f"You got {results[randint(1,2)]}!")
		else:
			headsTotal = 0
			tailsTotal = 0
			seq = []
			while headsTotal + tailsTotal < flips:
				seq.append(results[randint(1,2)])
				if seq[-1] == "Heads":
					headsTotal += 1
				else:
					tailsTotal += 1
			if flips < 210:
				await ctx.send(f"```{seq} \nHeads: {headsTotal} \nTails: {tailsTotal}```")
			else:
				await ctx.send(f"```Heads: {headsTotal} \nTails: {tailsTotal}```")
		
def setup(bot):
	bot.add_cog(Generators(bot))
	print("Generators Cog loaded")

def teardown(bot):
	print("Generators Cog unloaded")
	bot.remove_cog(Generators(bot))
