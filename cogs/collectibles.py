##-----imports-----##

import discord, random
from cogs import economy
from datetime import datetime, timedelta
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

##-----definitions-----##

inventories = {}
collections = {}
timeFormat = "%S:%M:%H/%d:%m:%Y"
cooldowns = {}

class Item():
	
	def __init__(self, itemData):
		self.id, self.name, self.description = itemData[0:3]
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
				if line == "":
					continue
				itemData = line.split("|")
				self.collection.append(Item(itemData))
		else:
			for line in fileData.split("\n"):
				if line == "":
					continue
				itemData = line.split("|")
				self.collection.append(Lootbox(itemData))

class Rarity():

	def __init__(self, name, colour, price):
		self.name = name
		self.colour = colour
		self.price = price
		self.icon = f"{name.lower()}_item"

	def fetch_emoji(self, server):
		self.emoji = discord.utils.get(server.emojis, name=self.icon)

class Rarities():

	common = Rarity("Common", discord.Color.light_grey(), 5)
	uncommon = Rarity("Uncommon", discord.Color.green(), 10)
	rare = Rarity("Rare", 0x6fa8dc, 20)
	legendary = Rarity("Legendary", discord.Color.dark_purple(), 50)
	exotic = Rarity("Exotic", discord.Color.gold(), 150)

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
	lootboxes = Collection("Lootboxes", "LOOT", "lootboxes.txt", True)

	collectionsList = [common, uncommon, rare, legendary, exotic, lootboxes]

##-----Errors-----##

class Error(Exception):
	pass

class ItemNotInInventory(Error):
	pass

class ItemNotFound(Error):
	pass

##-----Functions-----##

def find_item_by_id(id):
	for collection in Collections.collectionsList:
		item = discord.utils.get(collection.collection, id=id)
		if item != None:
			return item
	raise ItemNotFound

def find_collection_by_code(code):
	for collection in Collections.collectionsList:
		if collection.code == code:
			return collection
	return None

def search_for_lootbox(search):
	item = discord.utils.get(Collections.lootboxes.collection, id=search)
	if item != None:
		return item
	ref = {"common": "LOOT1", "uncommon" : "LOOT2", "rare" : "LOOT3", "legendary" : "LOOT4", "exotic" : "LOOT5"}
	if search in ref:
		return find_item_by_id(ref[search])
	return None

def check_cooldown(memberid, cooldownid, timer):
	if memberid not in cooldowns:
		dtnow = datetime.now()
		dthourly = dtnow - timedelta(hours = 1)
		dtdaily = dtnow - timedelta(days = 1)
		dtweekly = dtnow - timedelta(days = 7)
		cooldowns[memberid] = [dthourly, dtdaily, dtweekly]

	timeDifference = (datetime.now() - cooldowns[memberid][cooldownid]).total_seconds()
	if timeDifference > timer:
		cooldowns[memberid][cooldownid] = datetime.now()
		write_cooldowns_file()
		return True, timeDifference
	else:
		return False, timeDifference

def convert_td_to_string(td):
	seconds = int(td)
	days, seconds = seconds // (24*60*60), seconds % (24*60*60)
	hours, seconds = seconds // (60*60), seconds % (60*60)
	minutes, seconds = seconds // 60, seconds % 60

	outputString = ""
	if days != 0:
		outputString += f"{days} days, "
	if hours != 0:
		outputString += f"{hours} hours, "
	if minutes != 0:
		outputString += f"{minutes} minutes, "
	if outputString == "":
		outputString = f"{seconds} seconds"
	else:
		outputString = outputString[:-2] + f" and {seconds} seconds"
	return outputString

def add_to_collection(memberid, item):
	if memberid not in collections:
		collections[memberid] = []
	collections[memberid].append(item)
	write_collections_file()

def add_to_inventory(memberid, item):
	if memberid not in inventories:
		inventories[memberid] = []
	inventories[memberid].append(item)
	add_to_collection(memberid, item)
	write_inventories_file()

def remove_from_inventory(memberid, item):
	if memberid not in inventories:
		inventories[memberid] = []
	if item not in inventories[memberid]:
		raise ItemNotInInventory
	else:
		inventories[memberid].remove(item)
	write_inventories_file()


##-----Inventory Reading Functions-----##

def read_inventory_file():
	r = open(f"data/collectibles/inventories.txt", "r")
	fileData = r.read()
	r.close()

	inventories.clear()

	fileLines = fileData.split("\n")
	for line in fileLines:
		if line == "":
			continue
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
		if line == "":
			continue
		lineData = line.split(",")
		memberitems = []
		if len(lineData) > 1:
			for itemData in lineData[1:]:
				memberitems.append(find_item_by_id(itemData))
		collections[int(lineData[0])] = memberitems

def read_cooldowns_file():
	r = open(f"data/collectibles/cooldowns.txt", "r")
	fileData = r.read()
	r.close()

	cooldowns.clear()

	fileLines = fileData.split("\n")
	for line in fileLines:
		if line == "":
			continue
		lineData = line.split("|")
		memberStr, hourlyStr, dailyStr, weeklyStr = lineData
		hourlyObj = datetime.strptime(hourlyStr, timeFormat)
		dailyObj = datetime.strptime(dailyStr, timeFormat)
		weeklyObj = datetime.strptime(weeklyStr, timeFormat)
		cooldowns[int(memberStr)] = [hourlyObj, dailyObj, weeklyObj]

def load_all_files():
	read_inventory_file()
	read_collections_file()
	read_cooldowns_file()

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

def write_cooldowns_file():
	fileData = ""
	for member, datetimes in cooldowns.items():
		fileData += str(member)
		for dt in datetimes:
			fileData += "|" + dt.strftime(timeFormat)
		fileData += "\n"
	
	w = open(f"data/collectibles/cooldowns.txt", "w")
	w.write(fileData[:-1])
	w.close()

##-----Cog Code-----##	
	
class Collectibles(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		server = await self.bot.fetch_guild(ids.server)
		for rarity in list(Rarities.ref.values()):
			rarity.fetch_emoji(server)
		print("\n")
		for collection in list(Collections.collectionsList):
			print(f"Loaded {collection.name} collection with {len(collection.collection)} items.")

	@commands.command()
	async def item(self, ctx, itemid):
		try:
			item = find_item_by_id(itemid)
			await ctx.send(embed=item.generate_embed())
		except ItemNotFound:
			await ctx.send("Sorry, I couldn't find that item!")

	@commands.command(aliases=["i", "inv"])
	async def inventory(self, ctx):
		invData = inventories[ctx.author.id]
		inv = {}
		embed = discord.Embed()
		embed.title = f"{ctx.author.display_name}'s Inventory"
		embed.description = f"Balance: ${economy.get_user_balance(ctx.author.id)}"
		embed.set_thumbnail(url=ctx.author.avatar_url)
		for item in invData:
			if item.rarity not in inv:
				inv[item.rarity] = {}
			if item not in inv[item.rarity]:
				inv[item.rarity][item] = 0
			inv[item.rarity][item] += 1

		for rarity in list(Rarities.ref.values()):
			if rarity in inv:
				rarityItems = ""
				for item in inv[rarity]:
					rarityItems += f"{inv[rarity][item]}x {item.name} *({item.id})*\n"
				embed.add_field(name = f"{item.rarity.emoji}  {rarity.name}", value=rarityItems[:-1], inline=False)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_role(ids.roles["Mod"])
	async def additem(self, ctx, target : discord.Member, itemid):
		try:
			item = find_item_by_id(itemid.upper())
		except ItemNotFound:
			await ctx.send("Sorry, I couldn't find that item!")
			return
		add_to_inventory(target.id, item)
		await ctx.send(f"Added **{item.name}** to *{target.display_name}*'s inventory.")

	@commands.command()
	@commands.has_role(ids.roles["Mod"])
	async def removeitem(self, ctx, target : discord.Member, itemid):
		try:
			item = find_item_by_id(itemid.upper())
		except ItemNotFound:
			await ctx.send("Sorry, I couldn't find that item!")
			return
		try:
			remove_from_inventory(target.id, item)
		except ItemNotInInventory:
			await ctx.send(f"Couldn't find item in *{target.display_name}*'s inventory")
			return
		await ctx.send(f"Removed **{item.name}** from *{target.display_name}*'s inventory.")

	@commands.command()
	async def open(self, ctx, boxType):
		box = search_for_lootbox(boxType)
		if box == None:
			await ctx.send("I couldn't find that type of box :pensive:")
			return
		if ctx.author.id in inventories:
			try:
				inventories[ctx.author.id].remove(box)
				item = box.roll()
				inventories[ctx.author.id].append(item)
				write_inventories_file()
				
				embed = discord.Embed()
				embed.title = f"{box.name} opened!"
				embed.description = f"You got {item.rarity.emoji} *{item.name}*!"
				embed.color = item.rarity.colour

				await ctx.send(embed=embed)

			except ValueError:
				await ctx.send(f"Looks like you don't have any *{box.name}* :pensive:")
		else:
			await ctx.send(f"Looks like you don't have any *{box.name}* :pensive:")

	@commands.command()
	async def hourly(self, ctx):
		timeCheck, timeDifference = check_cooldown(ctx.author.id, 0, 60*60)
		if timeCheck == True:
			roll = random.randint(1,100)
			if roll < 85:
				lootbox = find_item_by_id("LOOT1")
			elif roll < 99:
				lootbox = find_item_by_id("LOOT2")
			else:
				lootbox = find_item_by_id("LOOT3")
			add_to_inventory(ctx.author.id, lootbox)
			await ctx.send(f"Success! You claimed a **{lootbox.name}**!")
		else:
			await ctx.send(f"Slow down there! You still have {convert_td_to_string(60*60 - timeDifference)} left before you can do that.")
			
	@commands.command()
	async def daily(self, ctx):
		timeCheck, timeDifference = check_cooldown(ctx.author.id, 1, 24*60*60)
		if timeCheck == True:
			roll = random.randint(1,100)
			if roll < 85:
				lootbox = find_item_by_id("LOOT2")
			elif roll < 99:
				lootbox = find_item_by_id("LOOT3")
			else:
				lootbox = find_item_by_id("LOOT4")
			add_to_inventory(ctx.author.id, lootbox)
			await ctx.send(f"Success! You claimed a **{lootbox.name}**!")
		else:
			await ctx.send(f"Slow down there! You still have {convert_td_to_string(24*60*60 - timeDifference)} left before you can do that.")
			
	@commands.command()
	async def weekly(self, ctx):
		timeCheck, timeDifference = check_cooldown(ctx.author.id, 2, 7*24*60*60)
		if timeCheck == True:
			roll = random.randint(1,100)
			if roll < 85:
				lootbox = find_item_by_id("LOOT3")
			elif roll < 99:
				lootbox = find_item_by_id("LOOT4")
			else:
				lootbox = find_item_by_id("LOOT5")
			add_to_inventory(ctx.author.id, lootbox)
			await ctx.send(f"Success! You claimed a **{lootbox.name}**!")
		else:
			await ctx.send(f"Slow down there! You still have {convert_td_to_string(7*24*60*60 - timeDifference)} left before you can do that.")

	@commands.command()
	async def claim(self, ctx, cooldown = "all"):
		cooldown = cooldown.lower()
		if cooldown in ["hour", "hourly"]:
			await ctx.invoke(self.bot.get_command('hourly'))
		elif cooldown in ["day", "daily"]:
			await ctx.invoke(self.bot.get_command('daily'))
		elif cooldown in ["week", "weekly"]:
			await ctx.invoke(self.bot.get_command('weekly'))
		elif cooldown in ["*", "all"]:
			await ctx.invoke(self.bot.get_command('daily'))
			await ctx.invoke(self.bot.get_command('hourly'))
			await ctx.invoke(self.bot.get_command('weekly'))
		else:
			await ctx.send(f"I'm afraid I don't understand '{cooldown}' :pensive:")

	@commands.command()
	async def sell(self, ctx, itemid):
		if itemid[:-1] == "LOOT":
			await ctx.send("I'm afraid you can't sell loot boxes!")
			return
		try:
			item = find_item_by_id(itemid)
		except ItemNotFound:
			await ctx.send("Sorry, I couldn't find that item!")
			return
		try:
			remove_from_inventory(ctx.author.id, item)
		except ItemNotInInventory:
			await ctx.send(f"It looks like you don't have an **{item.name}** :pensive:")
			return
		economy.add_user_balance(ctx.author.id, item.rarity.price)
		await ctx.send(f"You sold **{item.name}** for $*{item.rarity.price}*")





		
		
def setup(bot):
	load_all_files()
	bot.add_cog(Collectibles(bot))
	print("Collectibles Cog loaded")

def teardown(bot):
	print("Collectibles Cog unloaded")
	bot.remove_cog(Collectibles(bot))