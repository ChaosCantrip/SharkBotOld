import asyncpg
from discord.ext import tasks, commands
from handlers import curseHandler

class Curse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_update.start()

    def cog_unload(self):
        self.check_for_update.cancel()

    @tasks.loop(minutes=5)
    async def check_for_update(self):
        if curseHandler.check_new():
            modgen = await self.bot.fetch_channel(831595374337589289)
            await modgen.send("Vein Mining has been updated!")
            self.check_for_update.cancel()


def setup(bot):
    bot.add_cog(Curse(bot))
    print("Curse Cog loaded")


def teardown(bot):
    print("Curse Cog unloaded")
    bot.remove_cog(Curse(bot))