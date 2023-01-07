import json
from datetime import datetime

import discord
from discord.ext import tasks, commands
import SharkBot


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_database.start()

    def cog_unload(self) -> None:
        self.update_database.cancel()

    @tasks.loop(minutes=5)
    async def update_database(self):
        for member in SharkBot.Member.members.values():
            await member.fetch_discord_user(self.bot)
        changed_member_data = SharkBot.Database.check_differences()
        SharkBot.Database.write_snapshot()
        if len(changed_member_data) > 0:
            members_changed = len(changed_member_data)
            db_log_channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Database Log"])
            output_embed = discord.Embed()
            output_embed.title = "Database Upload Complete"
            output_embed.description = f"<t:{int(datetime.now().timestamp())}:D>\nUpdated {members_changed} members."
            for member_data in changed_member_data:
                SharkBot.Handlers.firestoreHandler.update_data(member_data["id"], member_data)
                output_embed.add_field(
                    name=member_data["display_name"] + "'s Data",
                    value=f"```{json.dumps(member_data, indent=2)}```",
                    inline=False
                )
            embeds = SharkBot.Utils.split_embeds(output_embed)
            for embed in embeds:
                await db_log_channel.send(embed=embed)


    @update_database.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    @update_database.error
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
