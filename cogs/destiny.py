import discord
from SharkBot import destiny
from discord.ext import tasks, commands

import secret

if secret.testBot:
	import testids as ids
else:
	import ids


class Destiny(commands.Cog):

	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@commands.hybrid_group()
	async def destiny(self, ctx: commands.Context) -> None:
		await ctx.send("Destiny Command")

	@destiny.command()
	async def sector(self, ctx: commands.Context) -> None:
		currentSector = destiny.LostSector.get_current()
		reward = destiny.LostSectorReward.get_current()

		embed = discord.Embed()
		embed.title = f"<:lost_sector_icon:1020115310050811948> {currentSector.name}"
		embed.add_field(
			name="Champions",
			value=currentSector.champion_list,
			inline=False
		)
		embed.add_field(
			name="Shields",
			value=currentSector.shield_list,
			inline=False
		)
		embed.add_field(
			name="Reward",
			value=reward.text,
			inline=False
		)

		await ctx.send(embed=embed)

	@destiny.command()
	async def sector_list(self, ctx: commands.Context) -> None:
		embed = discord.Embed()
		embed.title = "Lost Sectors"
		for lostSector in destiny.LostSector.lostSectors:
			embed.add_field(
				name=lostSector.name,
				value=f"Champions: *{lostSector.champion_list}*\nShields: *{lostSector.shield_list}*",
				inline=False
			)

		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Destiny(bot))
	print("Destiny Cog loaded")


async def teardown(bot):
	print("Destiny Cog unloaded")
	await bot.remove_cog(Destiny(bot))
