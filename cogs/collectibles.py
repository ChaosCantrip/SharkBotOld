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
	if id[0] in Collections.ref:
		collection = Collections.ref[id[0]].collection
		if id in collection:
			return collection[id]
		else:
			return None
	else:
		return None


##-----Inventory Reading Functions-----##

def fetch_member_line(file, memberid):
	r = open(f"data/collections/{file}")
	fileData = r.read()
	r.close()

	fileLines = fileData.split("\n")
	for line in fileLines:
		lineData = line.split(",")
		if lineData[0] == str(memberid):
			return lineData[1:]
	return None



def fetch_member_inventory_raw(memberid):
	return fetch_member_line("inventories.txt", memberid)



def fetch_member_collection_raw(memberid):
	return fetch_member_line("collections.txt", memberid)



def fetch_member_inventory(memberid):
	data = fetch_member_line("inventories.txt", memberid)
	outputData = []
	for itemid in data:
		outputData.append(find_item_by_id(itemid))



def fetch_member_collection(memberid):
	return fetch_member_line("collections.txt", memberid)
	outputData = []
	for itemid in data:
		outputData.append(find_item_by_id(itemid))

##-----Cog Code-----##

	
	
class Collectibles(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	def get_member_inventory(self, member):


	@commands.command()
	async def item(self, ctx, itemid):
		item = find_item_by_id(itemid)
		if item == None:
			await ctx.send("Sorry, that doesn't look like a valid ID.")
		else:
			await ctx.send(embed=item.generate_embed())
		
		
		
def setup(bot):
	bot.add_cog(Collectibles(bot))
	print("Collectibles Cog loaded")

def teardown(bot):
	print("Collectibles Cog unloaded")
	bot.remove_cog(Collectibles(bot))