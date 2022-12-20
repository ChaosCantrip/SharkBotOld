import json
from datetime import datetime

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
            print("There is data to upload")
            members_changed = len(data_to_change)
            records_changed = sum(len(d) for d in data_to_change.values())
            print(f"Updating {records_changed} records for {members_changed} members.")
            await SharkBot.Handlers.apiHandler.upload_data(data_to_change)
            print(f"Updated {records_changed} records for {members_changed} members.")
            db_log_channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Database Log"])
            embed = discord.Embed()
            embed.title = "Database Upload Complete"
            embed.description =  f"<t:{int(datetime.now().timestamp())}:D>"
            embed.add_field(
                name=f"Updated {records_changed} records for {members_changed} members.",
                value=f"```json\n{json.dumps(data_to_change, indent=2)}\n```"
            )
            await db_log_channel.send(embed=embed)
        else:
            print("No data to upload")

    @update_database.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    @update_database.error
    async def update_db_error(self, error: Exception):
        await SharkBot.Utils.task_loop_handler(self.bot, error)


async def setup(bot):
    await bot.add_cog(API(bot))
    print("API Cog loaded")


async def teardown(bot):
    print("API Cog unloaded")
    await bot.remove_cog(API(bot))
