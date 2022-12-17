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
        counts_to_change = SharkBot.API.check_changed_counts()
        if len(counts_to_change) > 0:
            for member in counts_to_change:
                discord_user = self.bot.get_user(member.id)
                if discord_user is None:
                    discord_user = await self.bot.fetch_user(member.id)
                    await SharkBot.Handlers.apiHandler.upload_counts(
                        member_id=member.id,
                        member_name=discord_user.display_name,
                        counts=member.counts
                    )
                print(member.id)


async def setup(bot):
    await bot.add_cog(API(bot))
    print("API Cog loaded")


async def teardown(bot):
    print("API Cog unloaded")
    await bot.remove_cog(API(bot))
