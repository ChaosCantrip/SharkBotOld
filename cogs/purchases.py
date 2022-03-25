import discord
from discord.ext import tasks, commands
from definitions import SharkErrors, Member

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

	
	
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
		
		
		
def setup(bot):
	bot.add_cog(Purchases(bot))
	print("Purchases Cog loaded")

def teardown(bot):
	print("Purchases Cog unloaded")
	bot.remove_cog(Purchases(bot))
