import io
import json
import logging
import os
from datetime import datetime
from typing import Optional

import discord
import psutil
from discord.ext import commands

import SharkBot

cog_logger = logging.getLogger("cog")

class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def update_manifest(self, ctx: commands.Context, force: bool = False):
        current_version = SharkBot.Destiny.Manifest.get_current_manifest()["Response"]["version"]
        embed=discord.Embed(
            title="Manifest Update",
            description=f"Force Update: {force}"
        )
        embed.add_field(
            name="Current Version",
            value=f"`{current_version}`",
            inline=False
        )
        embed.add_field(
            name="Checking for Update...",
            value="`Working on it...`",
            inline=False
        )
        message = await ctx.reply(embed=embed, mention_author=False)

        is_outdated = await SharkBot.Destiny.Manifest.is_outdated()
        if is_outdated:
            value = "`Manifest out of date.`"
        else:
            if force:
                value = "`Up to date... Force Updating`"
            else:
                value = "`Up to date`"
        embed.set_field_at(
            index=-1,
            name="New Manifest Retrieved",
            value=value,
            inline=False
        )
        await message.edit(embed=embed)
        if force or is_outdated:
            await SharkBot.Destiny.Manifest.update_manifest_async()
            new_version = SharkBot.Destiny.Manifest.get_current_manifest()["Response"]["version"]
            embed.add_field(
                name="Updated Manifest",
                value=f"`{new_version}`",
                inline=False
            )
            await message.edit(embed=embed)

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def react_to(self, ctx: commands.Context, target_message: discord.Message, *reactions: str):
        for reaction in reactions:
            await target_message.add_reaction(reaction)
        await ctx.reply(f"Reacted to `{target_message.content}` with {', '.join(reactions)}")

    @commands.command()
    @commands.is_owner()
    async def admin_clone_member(self, ctx: commands.Context, source_discord_member: discord.Member, target_discord_member: discord.Member):
        source_member = SharkBot.Member.get(source_discord_member.id, create=False)
        if source_member is None:
            await ctx.reply(f"{source_discord_member.mention} is not a SharkBot Member...")
            return
        target_member = SharkBot.Member.get(target_discord_member.id, create=False)
        if target_member is not None:
            await ctx.reply(f"{target_discord_member.mention} is already a SharkBot Member...")
            return
        source_data = json.loads(json.dumps(source_member.data))
        source_data["id"] = target_discord_member.id
        target_member = SharkBot.Member.Member(source_data)
        target_member.discord_user = target_discord_member
        target_member.register(with_write=True)
        await ctx.reply(f"Cloned {source_discord_member.mention} into {target_discord_member.mention}.")

    @commands.command()
    @commands.is_owner()
    async def admin_upload_items(self, ctx: commands.Context):
        f = lambda l: "```" + "\n".join(l) + "```"
        output_text = ["Working on it...\n"]
        message = await ctx.reply(f(output_text), mention_author=False)
        output_text.append("Collections")
        for collection in SharkBot.Collection.collections:
            SharkBot.Handlers.firestoreHandler.set_doc("collections", collection.id, collection.db_data)
            for item in collection.items:
                SharkBot.Handlers.firestoreHandler.set_doc("items", item.id, item.db_data)
            output_text.append(f"\t{collection.id} | {collection.name}... Done")
            await message.edit(content=f(output_text))
        output_text.append("\nRarities")
        for rarity in SharkBot.Rarity.rarities:
            SharkBot.Handlers.firestoreHandler.set_doc("rarities", rarity.name, rarity.db_data)
            output_text.append(f"\t{rarity.name}... Done")
            await message.edit(content=f(output_text))
        output_text.append("\n\nDone!")
        await message.edit(content=f(output_text))


    @commands.command()
    @commands.is_owner()
    async def get_member_data(self, ctx: commands.Context, discord_member: discord.Member):
        member = SharkBot.Member.get(discord_member.id, create=False)
        if member is None:
            await ctx.reply(f"{discord_member.mention} is not a SharkBot Member.")
            return
        member_file = f"{SharkBot.Member._MEMBERS_DIRECTORY}/{member.id}.json"
        file = discord.File(member_file)
        await ctx.reply(f"Member Data for {discord_member.mention}", file=file)

    @commands.command()
    @commands.is_owner()
    async def admin_delete_member(self, ctx: commands.Context, discord_member: discord.Member):
        member = SharkBot.Member.get(discord_member.id, create=False)
        if member is None:
            await ctx.reply(f"{discord_member.mention} is not a SharkBot Member.")
            return
        await ctx.invoke(self.bot.get_command("get_member_data"), discord_member=discord_member)
        member.remove()
        await ctx.reply(f"Removed {discord_member.mention} from SharkBot")

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def test_error(self, ctx: commands.Context) -> None:
        raise SharkBot.Errors.TestError()

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def list_members(self, ctx: commands.Context):
        content = []
        for i, member in enumerate(SharkBot.Member.members):
            content.append(f"{i+1}. {member.id} {member.display_name}")

        await ctx.reply("```" + "\n".join(content) + "```", mention_author=False)

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def list_member_files(self, ctx: commands.Context):
        content = []
        for i, filepath in enumerate(SharkBot.Utils.get_dir_filepaths("data/live/members")):
            filename = filepath.split("/")[-1]
            content.append(f"{i+1}. {filename}")

        await ctx.reply("```" + "\n".join(content) + "```", mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def get_bungie_data(self, ctx: commands.Context, components: commands.Greedy[int]):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        message = await ctx.reply("Sending Request...", mention_author=False)

        response = await member.bungie.get_endpoint_data(*components)
        file_io = io.BytesIO(json.dumps(response, indent=2).encode("utf-8"))
        file = discord.File(filename="response.json", fp=file_io)
        await message.edit(content="Response Received.", attachments=[file])
        file_io.close()

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def clean_members(self, ctx: commands.Context) -> None:
        user_ids = [user.id for user in self.bot.users]
        message_output = "Cleaning members...\n"
        message = await ctx.send(f"```{message_output}```")
        kept = 0
        removed = 0
        for member in list(SharkBot.Member.members):
            if member.id not in user_ids:
                message_output += f"\nRemoved {member.id}."
                await message.edit(content=f"```{message_output}```")
                member.remove()
                removed += 1
            else:
                kept += 1
        message_output += f"\n\nRemoved {removed} members, kept {kept}."
        await message.edit(content=f"```{message_output}```")
        SharkBot.Member.load_member_files()
        
    @commands.command()
    @commands.is_owner()
    async def get_emojis(self, ctx: commands.Context) -> None:
        output_text = "```Python\nicons = {"
        for emoji in ctx.guild.emojis:
            output_text += f'\n\t"{emoji.name}": "<:{emoji.name}:{emoji.id}>",'
        output_text = output_text[:-1] + "\n}\n```"
        await ctx.reply(output_text, mention_author=False)

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def system_status(self, ctx: commands.Context) -> None:
        vm = psutil.virtual_memory()

        total_mb = "{:,.2f} MB".format(vm.total/(1024*1024))
        total_gb = "{:,.2f} GB".format(vm.total/(1024*1024*1024))
        used_mb = "{:,.2f} MB".format(vm.used/(1024*1024))
        used_gb = "{:,.2f} GB".format(vm.used/(1024*1024*1024))
        free_mb = "{:,.2f} MB".format(vm.free/(1024*1024))
        free_gb = "{:,.2f} GB".format(vm.free/(1024*1024*1024))
        percent = f"{100-vm.percent}%"

        process = psutil.Process(os.getpid()).memory_info()
        process_mb = "{:,.2f} MB".format(process.rss / 1024 ** 2)
        process_gb = "{:,.2f} GB".format(process.rss / 1024 ** 3)
        process_percent_used = "{:,.2f}% Used".format((process.rss / vm.used) * 100)
        process_percent_total = "{:,.2f}% Total".format((process.rss / vm.total) * 100)

        embed = discord.Embed()
        embed.colour = discord.Color.greyple()
        embed.title = "System Status"
        embed.add_field(
            name="Total RAM",
            value=f"{total_mb}\n{total_gb}"
        )
        embed.add_field(
            name="Used RAM",
            value=f"{used_mb}\n{used_gb}"
        )
        embed.add_field(
            name="Free RAM",
            value=f"{free_mb}\n{free_gb}"
        )
        embed.add_field(
            name="Percentage Free RAM",
            value=f"{percent}"
        )
        embed.add_field(
            name="Used by Python",
            value=f"{process_mb}\n{process_gb}\n{process_percent_used}\n{process_percent_total}"
        )

        await ctx.send(embed=embed)

    @commands.hybrid_group()
    @SharkBot.Checks.is_mod()
    async def purge(self, ctx: commands.Context) -> None:
        await ctx.send("Purge Command")

    @purge.command()
    @SharkBot.Checks.is_mod()
    async def last(self, ctx: commands.Context, number: int) -> None:
        message = await ctx.reply(f"```Deleting last {number} messages.```")
        deleted = await ctx.channel.purge(limit=number, before=discord.Object(ctx.message.id))
        await message.edit(content=f"```Deleted last {len(deleted)} messages.```")

    @purge.command()
    @SharkBot.Checks.is_mod()
    async def to(self, ctx: commands.Context, target: discord.Message) -> None:
        message = await ctx.reply(f"```Deleting up to {target.id}.```")
        deleted = await ctx.channel.purge(before=discord.Object(ctx.message.id), after=discord.Object(target.id))
        await message.edit(content=f"```Deleted {len(deleted)} messages.")

    @purge.command()
    @SharkBot.Checks.is_mod()
    async def member(self, ctx: commands.Context, target: discord.Member, limit: int = 100) -> None:
        message = await ctx.reply(f"```Deleting messages from {target.display_name} in last {limit} messages.```")
        deleted = await ctx.channel.purge(
            limit=limit,
            check=lambda m: m.author.id == target.id,
            before=discord.Object(ctx.message.id)
        )
        await message.edit(content=f"```Deleted {len(deleted)} messages from {target.display_name}.```")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        with open("data/live/bot/lastmessage.txt", "w+") as outfile:
            outfile.write(datetime.strftime(datetime.now(), "%d/%m/%Y-%H:%M:%S:%f"))

    @commands.command()
    @commands.is_owner()
    async def write_members(self, ctx: commands.Context, upload: bool = False):
        for member in SharkBot.Member.members:
            member.write_data(upload=upload)
        await ctx.reply(f"Saved data for {len(SharkBot.Member.members)} Members.", mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def wipe_bungie_cache(self, ctx: commands.Context):
        message = await ctx.reply("```Working on it...```", mention_author=False)
        for member in SharkBot.Member.members:
            member.bungie.wipe_all_cache()
        await message.edit(content="```Done!```")

    @commands.command()
    @commands.is_owner()
    async def send_embed(self, ctx: commands.Context, target_channel: Optional[discord.TextChannel] = None, with_timestamp: bool = True, with_author: bool = True):
        if len(ctx.message.attachments) == 0:
            await ctx.reply("Where file?")
        if target_channel is None:
            target_channel = ctx.channel
        num = 0
        for attachment in ctx.message.attachments:
            attachment_data = await attachment.read()
            embed_data = json.loads(attachment_data)
            embed = discord.Embed.from_dict(embed_data)
            if with_timestamp:
                if embed.timestamp is None:
                    embed.timestamp = datetime.now()
            if with_author:
                if embed.author is None:
                    embed.set_author(
                        name=ctx.author.name,
                        icon_url=ctx.author.display_avatar.url
                    )
            await target_channel.send(embed=embed)
            num += 1
        if target_channel != ctx.channel:
            await ctx.reply(f"Sent `{num+1}` Embeds to {target_channel.mention}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("Admin Cog Loaded")
    cog_logger.info("Admin Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Admin(bot))
    print("Admin Cog Unloaded")
    cog_logger.info("Admin Cog Unloaded")