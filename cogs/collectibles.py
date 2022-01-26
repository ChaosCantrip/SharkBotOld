##-----imports-----##

import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids



##-----definitions-----##

class Item():
	
	def __init__(self, itemData):
		self.id, self.name, self.description = itemData[0:3]
		self.price = int(itemData[-1])
		self.rarity = Rarities.ref[self.id[0]]

		self.embed = discord.Embed



class Collection():
	
	def __init__(self, rarity, filename):
		self.name = rarity.name
		self.colour = rarity.colour
		self.rarity = rarity
		
		r = open(f"collectibles/{filename}", "r")
		fileData = r.read()
		r.close()

		self.collection = {}
		for line in fileData.split("\n"):
			print(line)
			itemData = line.split(";")
			print(itemData)
			self.collection[itemData[0]] = Item(itemData)



class Rarity():

	def __init__(self, name, colour):
		self.name = name
		self.colour = colour



class Rarities():

	common = Rarity("Common", "#808080")
	uncommon = Rarity("Uncommon", "#90ee90")
	rare = Rarity("Rare", "#B9CFF0")
	legendary = Rarity("Legendary", "#CC8899")
	exotic = Rarity("Exotic", "#FFD300")

	ref = {
		"C" : common,
		"U" : uncommon,
		"R" : rare,
		"L" : legendary,
		"E" : exotic}



class Collections():

	common = Collection(Rarities.common, "common.txt")
	uncommon = Collection(Rarities.uncommon, "uncommon.txt")
	rare = Collection(Rarities.rare, "rare.txt")
	legendary = Collection(Rarities.legendary, "legendary.txt")
	exotic = Collection(Rarities.exotic, "exotic.txt")



##-----Cog Code-----##

	
	
class Collectibles(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
		
		
def setup(bot):
	bot.add_cog(Collectibles(bot))
	print("Collectibles Cog loaded")

def teardown(bot):
	print("Collectibles Cog unloaded")
	bot.remove_cog(Collectibles(bot))