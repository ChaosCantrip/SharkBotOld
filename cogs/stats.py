import discord
from discord.ext import tasks, commands

import secret
from SharkBot import Member

if secret.testBot:
	import testids as ids
else:
	import ids


class Stats(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command()
	async def stats(self, ctx: commands.Context):
		member = Member.get(ctx.author.id)

		embed = discord.Embed()
		embed.title = "Your Stats"
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
		embed.set_thumbnail(url=ctx.author.avatar.url)
		embed.description = f"Counts: `{member.counts}`"
		embed.description += f"\nIncorrect Counts: `{member.stats.incorrectCounts}`"
		embed.description += f"\nCoinflip KDA: `{member.stats.coinflipkda}`"
		embed.description += f"\nCoinflip Win Rate: `{member.stats.coinflipwinrate}%`"
		embed.description += f"\nClaimed Boxes: `{member.stats.claimedBoxes}`"
		embed.description += f"\nBought Boxes: `{member.stats.boughtBoxes}`"
		embed.description += f"\nOpened Boxes: `{member.stats.openedBoxes}`"
		embed.description += f"\nBoxes from Counting: `{member.stats.countingBoxes}`"
		embed.description += f"\nSold Items: `{member.stats.soldItems}`"
		embed.description += f"\nMissions Completed: `{member.stats.completedMissions}`"
		embed.set_footer(text="Stats began tracking on 04/09/2022")

		await ctx.send(embed=embed)



async def setup(bot):
	await bot.add_cog(Stats(bot))
	print("Stats Cog loaded")


async def teardown(bot):
	print("Stats Cog unloaded")
	await bot.remove_cog(Stats(bot))
