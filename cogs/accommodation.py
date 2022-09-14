import discord
from discord.ext import tasks, commands
from handlers import websiteChecker

import secret

if secret.testBot:
	import testids as ids
else:
	import ids


class Accommodation(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.check_website.start()

	def cog_unload(self) -> None:
		self.check_website.cancel()

	@tasks.loop(seconds=10)
	async def check_website(self):
		siteData = websiteChecker.get_site()
		siteHash = websiteChecker.convert_to_hash(siteData)
		newSite = websiteChecker.check_new_hash(siteHash)

		if newSite:
			chaos = self.bot.get_user(ids.users["Chaos"])
			embed = discord.Embed()
			embed.title = "New Hash Detected"
			embed.description = siteHash
			embed.url = websiteChecker.url

			await chaos.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Accommodation(bot))
	print("Accommodation Cog loaded")


async def teardown(bot):
	print("Accommodation Cog unloaded")
	await bot.remove_cog(Accommodation(bot))
