from discord.ext import tasks, commands
import discord
from handlers import curseHandler
from datetime import datetime

class Curse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_update.start()

    def cog_unload(self):
        self.check_for_update.cancel()

    @tasks.loop(minutes=5)
    async def check_for_update(self):
        result = curseHandler.check_new()
        with open("data/curse.txt", "a") as curseFile:
            curseFile.write(f"{datetime.strftime(datetime.now(), '%m/%d/%Y, %H:%M:%S')} - {result}\n")
        if result:
            modgen = await self.bot.fetch_channel(831595374337589289)
            await modgen.send("Vein Mining has been updated!")
            self.check_for_update.cancel()

    @commands.command()
    @commands.has_role(684446526453710926)
    async def check_curse(self, ctx):
        result = curseHandler.check_new()
        with open("data/curse.txt", "a") as curseFile:
            curseFile.write(f"{datetime.strftime(datetime.now(), '%m/%d/%Y, %H:%M:%S')} - {result}\n")
        with open("data/curse.txt", "rb") as curseFile:
            await ctx.send("Here's the file!", file=discord.File(curseFile))


def setup(bot):
    bot.add_cog(Curse(bot))
    print("Curse Cog loaded")


def teardown(bot):
    print("Curse Cog unloaded")
    bot.remove_cog(Curse(bot))