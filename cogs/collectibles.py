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

	def generate_embed(self):
		embed = discord.Embed()
		embed.title = self.name
		embed.color = self.rarity.colour
		embed.description = self.description
		embed.set_footer(text = f"{self.rarity.name} | {self.id}")

		return embed



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
			itemData = line.split(";")
			self.collection[itemData[0]] = Item(itemData)



class Rarity():

	def __init__(self, name, colour):
		self.name = name
		self.colour = colour



class Rarities():

	common = Rarity("Common", discord.Color.light_grey())
	uncommon = Rarity("Uncommon", discord.Color.green())
	rare = Rarity("Rare", 0x6fa8dc)
	legendary = Rarity("Legendary", discord.Color.dark_purple())
	exotic = Rarity("Exotic", discord.Color.gold())

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

	ref = {
		"C" : common,
		"U" : uncommon,
		"R" : rare,
		"L" : legendary,
		"E" : exotic}





##-----Functions-----##

def find_item_by_id(id):
	if id[0] in Rarities.ref:
		collection = Collections.ref[id[0]]
		if id in collection:
			return collection[id]
		else:
			return None
	else:
		return None

##-----Cog Code-----##

	
	
class Collectibles(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def item(self, ctx, itemid):
		item = find_item_by_id(itemid)
		if item == None:
			ctx.send("Sorry, that doesn't look like a valid ID.")
		else:
			ctx.send(embed=item.generate_embed())
		
		
		
def setup(bot):
	bot.add_cog(Collectibles(bot))
	print("Collectibles Cog loaded")

def teardown(bot):
	print("Collectibles Cog unloaded")
	bot.remove_cog(Collectibles(bot))