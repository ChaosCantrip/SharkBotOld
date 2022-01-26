class Item():
	
	def __init__(self, itemData):
		self.id, self.name, self.description = itemData
		self.price = int(itemData[-1])
		self.rarity = Rarities.ref[self.id[0]]



class Collection():
	
	def __init__(self, rarity, file):
		self.name = rarity.name
		self.colour = rarity.colour
		self.rarity = rarity
		
		r = open(file, "r")
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
	
	def __init__(self):
		self.common = Rarity("Common", "#808080")
		self.uncommon = Rarity("Uncommon", "#90ee90")
		self.rare = Rarity("Rare", "#B9CFF0")
		self.legendary = Rarity("Legendary", "#CC8899")
		self.exotic = Rarity("Exotic", "#FFD300")



class Collections():

	def __init__(self):
		self.common = Collection(Rarities.common, "common.txt")
		self.uncommon = Collection(Rarities.uncommon, "uncommon.txt")
		self.rare = Collection(Rarities.rare, "rare.txt")
		self.legendary = Collection(Rarities.legendary, "legendary.txt")
		self.exotic = Collection(Rarities.exotic, "exotic.txt")


