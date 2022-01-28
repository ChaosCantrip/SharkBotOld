##-----imports-----##

import discord, random
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
		self.price = int(itemData[4])
		self.rarity = Rarities.ref[itemData[3]]

	def generate_embed(self):
		embed = discord.Embed()
		embed.title = self.name
		embed.color = self.rarity.colour
		embed.description = self.description
		embed.set_footer(text = f"{self.rarity.name} | {self.id}")

		return embed

class Lootbox(Item):

	def __init__(self, itemData):
		super().__init__(itemData[:-1])
		self.lootPoolCode = itemData[-1]

	def roll(self):

		self.lootPool = {}
		lootPoolCodes = self.lootPoolCode
		cumulativeChance = 0
		lootCodeList = lootPoolCodes.split(";")
		for code in lootCodeList:
			codeData = code.split(":")

			collection = find_collection_by_code(codeData[0])
			itemSet = collection.collection
			cumulativeChance += int(codeData[1])
			self.lootPool[cumulativeChance] = itemSet

		d100 = random.randint(1,100)
		for chance, pool in self.lootPool.items():
			if d100 < chance:
				return pool[random.randint(0,len(pool)-1)]

class Collection():
	
	def __init__(self, name, code, filename, lootbox=False):
		self.name = name
		self.code = code
		
		r = open(f"collectibles/{filename}", "r")
		fileData = r.read()
		r.close()

		self.collection = []

		if lootbox == False:
			for line in fileData.split("\n"):
				itemData = line.split("|")
				self.collection.append(Item(itemData))
		else:
			for line in fileData.split("\n"):
				itemData = line.split("|")
				self.collection.append(Lootbox(itemData))

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
		"common" : common,
		"uncommon" : uncommon,
		"rare" : rare,
		"legendary" : legendary,
		"exotic" : exotic}

class Collections():

	common = Collection("Common", "C", "common.txt")
	uncommon = Collection("Uncommon", "U", "uncommon.txt")
	rare = Collection("Rare", "R", "rare.txt")
	legendary = Collection("Legendary", "L", "legendary.txt")
	exotic = Collection("Exotic", "E", "exotic.txt")
	lootboxes = Collection("Lootboxes", "LBOX", "lootboxes.txt", True)

	collectionsList = [common, uncommon, rare, legendary, exotic, lootboxes]

##-----Functions-----##



def find_item_by_id(id):
	for collection in Collections.collectionsList:
		item = discord.utils.get(collection.collection, id=id)
		if item != None:
			return item
	return None

def find_collection_by_code(code):
	for collection in Collections.collectionsList:
		if collection.code == code:
			return collection
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



	@commands.command()
	@commands.has_role(ids.roles["Mod"])
	async def additem(self, ctx, target : discord.Member, itemid):
		item = find_item_by_id(itemid.upper())
		if target.id in inventories:
			inventories[target.id].append(item)
		else:
			inventories[target.id] = [item]
		write_inventories_file()
		await ctx.send(f"Added **{item.name}** to *{target.display_name}*'s inventory.")



	@commands.command()
	@commands.has_role(ids.roles["Mod"])
	async def removeitem(self, ctx, target : discord.Member, itemid):
		item = find_item_by_id(itemid.upper())
		if target.id in inventories:
			try:
				inventories[target.id].remove(item)
			except ValueError:
				await ctx.send(f"Item not found in *{target.display_name}*'s inventory.")
		else:
			await ctx.send(f"Item not found in *{target.display_name}*'s inventory.")
		write_inventories_file()
		await ctx.send(f"Removed **{item.name}** from *{target.display_name}*'s inventory.")

	@commands.command()
	async def test(self, ctx):
		item = find_item_by_id("LOOT1").roll()
		await ctx.send(embed=item.generate_embed())

		
		
def setup(bot):
	read_inventory_file()
	read_collections_file()
	bot.add_cog(Collectibles(bot))
	print("Collectibles Cog loaded")

def teardown(bot):
	print("Collectibles Cog unloaded")
	bot.remove_cog(Collectibles(bot))