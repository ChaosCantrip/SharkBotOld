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
            response = await SharkBot.Handlers.apiHandler.upload_data(data_to_change)
            members_changed = len(data_to_change)
            records_changed = sum(len(d) for d in data_to_change.values())
            db_log_channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Database Log"])
            output_embed = discord.Embed()
            output_embed.title = "Database Upload Complete"
            output_embed.description = f"<t:{int(datetime.now().timestamp())}:D>"
            output_embed.set_footer(text=f"Status Code: {response}")
            output_embed.add_field(
                name=f"Updated {records_changed} records for {members_changed} members.",
                value=f"```json\n{json.dumps(data_to_change, indent=2)}\n```"
            )
            embeds = SharkBot.Utils.split_embeds(output_embed)
            for embed in embeds:
                await db_log_channel.send(embed=embed)

            if response != 201:
                dev = self.bot.fetch_user(SharkBot.IDs.dev)
                await dev.send("FUCK")

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
        await SharkBot.Handlers.apiHandler.upload_data({
            str(member.id): member.snapshot_data
        })
        await message.edit(content=message.content + " Done.")

    @commands.command()
    @commands.is_owner()
    async def force_upload_all(self, ctx: commands.Context):
        num = len(SharkBot.Member.members)
        message = await ctx.reply(f"Uploading all member data... (0/{num})")
        for i, member in enumerate(SharkBot.Member.members.values()):
            await message.edit(content=f"Uploading all member data... ({i+1}/{num})\n`{member.id}`")
            await SharkBot.Handlers.apiHandler.upload_data({
                str(member.id): member.snapshot_data
            })
        await message.edit(content=f"Uploaded all member data for {num} members.")


async def setup(bot):
    await bot.add_cog(API(bot))
    print("API Cog loaded")


async def teardown(bot):
    print("API Cog unloaded")
    await bot.remove_cog(API(bot))
