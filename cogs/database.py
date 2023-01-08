import json
from datetime import datetime

import discord
from discord.ext import tasks, commands
import SharkBot


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.database_loop.start()

    def cog_unload(self) -> None:
        self.database_loop.cancel()

    @tasks.loop(minutes=5)
    async def database_loop(self):

        messages = []

        for member in SharkBot.Member.members.values():
            await member.fetch_discord_user(self.bot)
            if member.snapshot_has_changed:
                messages.append(member.upload_data(force_upload=True))

        if len(messages) > 0:
            embed = discord.Embed()
            embed.title = "Database Update"
            embed.description = f"<t:{int(datetime.now().timestamp())}:D>\n"
            embed.description += "```" + "\n".join(messages) + "```"

            db_log_channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Database Log"])
            await db_log_channel.send(embed=embed)


    @database_loop.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    @database_loop.error
    async def update_db_error(self, error: Exception):
        await SharkBot.Utils.task_loop_handler(self.bot, error)

    @commands.command()
    @commands.is_owner()
    async def force_upload(self, ctx: commands.Context, target: discord.Member):
        member = SharkBot.Member.get(target.id)
        message = await ctx.reply(f"Uploading data for {target.mention}...")
        await SharkBot.Handlers.firestoreHandler.update_data(member.id, member.snapshot_data)
        await message.edit(content=message.content + " Done.")

    @commands.command()
    @commands.is_owner()
    async def force_upload_all(self, ctx: commands.Context):
        num = len(SharkBot.Member.members)
        message = await ctx.reply(f"Uploading all member data... (0/{num})")
        for i, member in enumerate(SharkBot.Member.members.values()):
            await message.edit(content=f"Uploading all member data... ({i+1}/{num})\n`{member.id}`")
            await SharkBot.Handlers.firestoreHandler.update_data(member.id, member.snapshot_data)
        await message.edit(content=f"Uploaded all member data for {num} members.")


async def setup(bot):
    await bot.add_cog(Database(bot))
    print("Database Cog loaded")


async def teardown(bot):
    print("Database Cog unloaded")
    await bot.remove_cog(Database(bot))
