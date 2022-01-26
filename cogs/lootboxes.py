import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids



def read_inventories():
    r = open("inventories.txt", "r")
    fileData = r.read()
    r.close()

    split1 = fileData.split("\n")
    split2 = {}
    for line in split1:
        userid, invData = item.split(":")
        inv = invData.split(",")
        split2[int(userid)] = inv

    return split2



class Item():

	def __init__(self, itemData):
		self.id, self.name, self.description, self.price = itemData


	
class Lootboxes(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot



		
		
		
def setup(bot):
	bot.add_cog(Lootboxes(bot))
	print("Lootboxes Cog loaded")

def teardown(bot):
	print("Lootboxes Cog unloaded")
	bot.remove_cog(Lootboxes(bot))
