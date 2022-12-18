import discord
from discord.ext import tasks, commands
import SharkBot


class API(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_database.start()

    def cog_unload(self) -> None:
        self.update_database.cancel()

    @tasks.loop(minutes=5)
    async def update_database(self):
        for member in SharkBot.Member.members.values():
            await member.fetch_discord_user(self.bot)
        data_to_change = SharkBot.API.check_differences()
        SharkBot.API.write_snapshot()
        if len(data_to_change) > 0:
            await SharkBot.Handlers.apiHandler.upload_data(data_to_change)

    @update_database.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(API(bot))
    print("API Cog loaded")


async def teardown(bot):
    print("API Cog unloaded")
    await bot.remove_cog(API(bot))
