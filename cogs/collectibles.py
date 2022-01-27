##-----imports-----##

import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

##-----definitions-----##

inventories = {}
collections = {}

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
		self.icon = name.lower() + "_item"



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
	if id[0] in Collections.ref:
		collection = Collections.ref[id[0]].collection
		if id in collection:
			return collection[id]
		else:
			return None
	else:
		return None



##-----Inventory Reading Functions-----##

def read_inventory_file():
	r = open(f"data/collectibles/inventories.txt", "r")
	fileData = r.read()
	r.close()

	inventories.clear()

	fileLines = fileData.split("\n")
	for line in fileLines:
		lineData = line.split(",")
		memberitems = []
		if len(lineData) > 1:
			for itemData in lineData[1:]:
				memberitems.append(find_item_by_id(itemData))
		inventories[int(lineData[0])] = memberitems



def read_collections_file():
	r = open(f"data/collectibles/collections.txt", "r")
	fileData = r.read()
	r.close()

	collections.clear()

	fileLines = fileData.split("\n")
	for line in fileLines:
		lineData = line.split(",")
		memberitems = []
		if len(lineData) > 1:
			for itemData in lineData[1:]:
				memberitems.append(find_item_by_id(itemData))
		collections[int(lineData[0])] = memberitems


##-----File Writing Functions-----##


def write_inventories_file():
	fileData = ""
	for member, items in inventories.items():
		fileData += str(member)
		for item in items:
			fileData += "," + item.id
		fileData += "\n"
	
	w = open(f"data/collectibles/inventories.txt", "w")
	w.write(fileData[:-1])
	w.close()

def write_collections_file():
	fileData = ""
	for member, items in collections.items():
		fileData += str(member)
		for item in items:
			fileData += "," + item.id
		fileData += "\n"
	
	w = open(f"data/collectibles/collections.txt", "w")
	w.write(fileData[:-1])
	w.close()

##-----Cog Code-----##

	
	
class Collectibles(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot



	@commands.command()
	async def item(self, ctx, itemid):
		item = find_item_by_id(itemid)
		if item == None:
			await ctx.send("Sorry, that doesn't look like a valid ID.")
		else:
			await ctx.send(embed=item.generate_embed())



	@commands.command(aliases=["i", "inv"])
	async def inventory(self, ctx):
		inv = inventories[ctx.author.id]
		embed = discord.Embed()
		embed.title = f"{ctx.author.display_name}'s Inventory"
		embed.set_thumbnail(url=ctx.author.avatar_url)
		for item in inv:
			embed.add_field(name = f"{discord.utils.get(ctx.message.guild.emojis, name=item.rarity.icon)}  {item.name}", value=item.description, inline=False)
		await ctx.send(embed=embed)

		
		
def setup(bot):
	read_inventory_file()
	read_collections_file()
	bot.add_cog(Collectibles(bot))
	print("Collectibles Cog loaded")

def teardown(bot):
	print("Collectibles Cog unloaded")
	bot.remove_cog(Collectibles(bot))