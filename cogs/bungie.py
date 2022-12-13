import aiohttp
import discord
from discord.ext import tasks, commands

import secret
from SharkBot import IDs

found_codes = []


class Bungie(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.check_bungie_api.start()

    async def cog_unload(self) -> None:
        self.check_bungie_api.cancel()

    @tasks.loop(minutes=5)
    async def check_bungie_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=secret.Bungie.url, headers=secret.Bungie.headers) as r:
                status = r.status

        if status not in found_codes:
            found_codes.append(status)
            channel = await self.bot.fetch_channel(966046820943945748)

            embed = discord.Embed()
            embed.title = f"New Bungie API Status Code - {status}"
            embed.description = f"The Bungie API may be back online, this code should be 200 if it is."

            await channel.send(embed=embed)

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def enable_api_check(self, ctx: commands.Context):
        if self.check_bungie_api.is_running():
            await ctx.send("Loop is already running!")
        else:
            self.check_bungie_api.start()
            await ctx.send("Started Bungie API checking loop")

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def disable_api_check(self, ctx: commands.Context):
        if not self.check_bungie_api.is_running():
            await ctx.send("Loop is already disabled!")
        else:
            self.check_bungie_api.cancel()
            await ctx.send("Disabled Bungie API checking loop")

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def api_check(self, ctx: commands.Context):
        await ctx.send(str(self.check_bungie_api.is_running()))


async def setup(bot):
    await bot.add_cog(Bungie(bot))
    print("Bungie Cog loaded")


async def teardown(bot):
    print("Bungie Cog unloaded")
    await bot.remove_cog(Bungie(bot))
