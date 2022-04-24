import discord
from discord.ext import tasks, commands
from definitions import SharkErrors, Member, Order
from woocommerce import API
from cogs import collectibles

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

wcapi = API(
	url="https://sharkbot.co.uk",
	consumer_key=secret.wc_consumer_key,
	consumer_secret=secret.wc_consumer_secret,
	version="wc/v3"
)
	
class Purchases(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def link(self, ctx, account):
		member = Member.get(ctx.author.id)
		if ctx.channel.type is not discord.ChannelType.private:
			await ctx.message.delete()
			await ctx.send("Don't put your email address in a public server, silly billy! I'll DM you from here.")
		try:
			member.link_account(account)
		except SharkErrors.AccountAlreadyLinkedError:
			await ctx.author.send(f"Your id is already linked to **{member.linked_account}**! If you need to link it to a different email address, try *$unlink* first.")
			return
		except SharkErrors.AccountAlreadyInUseError:
			await ctx.author.send(f"**account** is already in use. If you believe this to be an error, please contact a Shark Exorcist Moderator.")
			return
		await ctx.author.send(f"SharkBot Account linked to **{member.linked_account}**")


	@commands.command()
	async def unlink(self, ctx):
		member = Member.get(ctx.author.id)
		try:
			member.unlink_account()
		except SharkErrors.AccountNotLinkedError:
			await ctx.send("Your SharkBot Account isn't linked to an email address!")
			return
		await ctx.send(f"SharkBot Account unlinked from your email address!")
		

	@commands.command()
	async def redeem(self, ctx):
		member = Member.get(ctx.author.id)

		if member.linked_account == None:
			await ctx.send("Your SharkBot account isn't linked to an email address! Try using $link <email> first!")
			return

		orderData = wcapi.get("orders").json()
		print(orderData)
		orders = []

		for data in orderData:
			order = Order.Order(data)
			if order.status == "processing" and order.email == member.linked_account:
				orders.append(order)

		if orders == []:
			await ctx.send("You don't have any pending orders!")
			return

		for order in orders:
			embed = discord.Embed()
			embed.title = f"Order #{order.id}"
			embed.description = ""
			print(order.items)

			for product in order.items:
				embed.description += f"{product.quantity}x **{product.product_name}**\n"
				items, cash = get_items(product.product_id)
				for i in range(0, product.quantity):
					member.add_items_to_inventory(items)
					member.add_balance(cash)

			embed.description = embed.description[:-1]
			await ctx.send(embed=embed)

			update = wcapi.post(f"orders/{order.id}", {"status":"completed"})
			order.status = "completed"

def get_items(product_id):
	items = []
	cash = 0
	if product_id == 62:
		items.append("LOOT1")
		for item in range(0,1):
			items.append("LOOT11")
		cash += 20
	elif product_id == 56:
		items.append("LOOT2")
		for item in range(0,3):
			items.append("LOOT11")
		cash += 40
	elif product_id == 57:
		items.append("LOOT3")
		for item in range(0,5):
			items.append("LOOT11")
		cash += 80
	elif product_id == 58:
		items.append("LOOT4")
		for item in range(0,10):
			items.append("LOOT11")
		cash += 160
	elif product_id == 59:
		items.append("LOOT5")
		for item in range(0,25):
			items.append("LOOT11")
		cash += 320
	elif product_id == 60:
		items.append("LOOT10")
		for item in range(0,50):
			items.append("LOOT11")
		cash += 640
	rawitems = items
	items = []
	for itemid in rawitems:
		items.append(collectibles.find_item_by_id(itemid))
	return items, cash

def setup(bot):
	bot.add_cog(Purchases(bot))
	print("Purchases Cog loaded")

def teardown(bot):
	print("Purchases Cog unloaded")
	bot.remove_cog(Purchases(bot))
