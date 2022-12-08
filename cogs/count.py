import json
import os
from datetime import datetime, timedelta, date
from typing import Union

import discord
import humanize
from discord.ext import commands, tasks

from SharkBot import Member, Item, IDs, Lootpool, Utils


def convert_to_num(message: discord.Message) -> Union[int, None]:
    result = ""

    content = str(message.clean_content)
    while "<" in content and ">" in content:
        start = content.index("<")
        end = content.index(">") + 1
        content = content[:start] + content[end:]

    for char in content:
        if char.isdigit():
            result = result + char

    if result == "":
        return None
    else:
        return int(result)


async def get_last_count(message: discord.Message) -> Union[discord.Message, None]:
    async for past_message in message.channel.history(limit=20, before=message):
        if past_message.author.id not in IDs.blacklist and convert_to_num(past_message) is not None:
            return past_message
    return None


async def get_last_member_count(message) -> Union[discord.Message, None]:
    async for pastMessage in message.channel.history(limit=20, before=message):
        if pastMessage.author.id is not message.author.id:
            continue
        return pastMessage
    return None


class Count(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.count_cleanup.start()

    def cog_unload(self) -> None:
        self.count_cleanup.cancel()

    @tasks.loop(minutes=15)
    async def count_cleanup(self):
        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        if os.path.exists("data/live/bot/count_cleanup.txt"):
            try:
                with open("data/live/bot/count_cleanup.txt", "r") as infile:
                    last_checked = discord.Object(id=int(infile.read()))
            except ValueError:
                last_checked = None
        else:
            last_checked = None

        check_to = datetime.utcnow() - timedelta(minutes=15)

        deleted = await channel.purge(
            limit=None,
            check=lambda m: m.author.id in IDs.blacklist,
            before=check_to,
            after=last_checked,
            oldest_first=True,
            bulk=False,
            reason="Count Cleanup"
        )

        if len(deleted) > 0:
            with open("data/live/bot/count_cleanup.txt", "w+") as outfile:
                outfile.write(str(deleted[-1].id))

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def check_counts(self, ctx: commands.Context):
        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        reply_text = ["Ok! Checking counts!\n", "0 messages checked!"]
        reply_message = await ctx.reply("```" + "\n".join(line for line in reply_text) + "```", mention_author=False)

        count = 0
        difference = 1
        errors = []
        i = 0
        last_mistake = None
        async for message in channel.history(limit=None, oldest_first=True):
            i += 1
            if message.author.id in IDs.blacklist:
                continue
            message_count = convert_to_num(message)
            if message_count is None:
                errors.append(
                    {
                        "author_name": message.author.display_name,
                        "author_id": message.author.id,
                        "timestamp": message.created_at.isoformat(),
                        "message_id": message.id,
                        "message_link": message.jump_url,
                        "content": message.content,
                        "error": "Not a count"
                    }
                )
            elif message_count != count + difference:

                if last_mistake is None:
                    last_mistake = message_count
                    errors.append(
                        {
                            "author_name": message.author.display_name,
                            "author_id": message.author.id,
                            "timestamp": message.created_at.isoformat(),
                            "message_id": message.id,
                            "message_link": message.jump_url,
                            "content": message.content,
                            "error": f"Expected count: {count + difference}"
                        }
                    )
                elif message_count != last_mistake and message_count != last_mistake + 2:
                    errors.append(
                        {
                            "author_name": message.author.display_name,
                            "author_id": message.author.id,
                            "timestamp": message.created_at.isoformat(),
                            "message_id": message.id,
                            "message_link": message.jump_url,
                            "content": message.content,
                            "error": f"Expected count: {count + difference}"
                        }
                    )
                else:
                    last_mistake = None

                count = message_count
            else:
                count = message_count

            if i % 200 == 0:
                reply_text[-1] = f"{i} messages checked, {len(errors)} errors found..."
                await reply_message.edit(content="```" + "\n".join(line for line in reply_text) + "```")

        with open("data/live/bot/count_errors.json", "w+") as outfile:
            json.dump(errors, outfile, indent=4)

        reply_text[-1] = f"{i} messages checked..."
        reply_text.append(f"\nDone! {len(errors)} errors found!")

        if len(errors) > 0:
            with open("data/live/bot/count_errors.json", "rb") as infile:
                file = discord.File(infile)
            await reply_message.edit(content="```" + "\n".join(line for line in reply_text) + "```", attachments=[file])
        else:
            await reply_message.edit(content="```" + "\n".join(line for line in reply_text) + "```")

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def clean_not_counts(self, ctx: commands.Context):
        if not os.path.exists("data/live/bot/count_errors.json"):
            await ctx.reply("The errors file doesn't exist!", mention_author=False)
            return

        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        with open("data/live/bot/count_errors.json", "r") as infile:
            error_file_data = json.load(infile)

        errors_to_clean = [error for error in error_file_data if error["error"] == "Not a count"]

        reply_text = ["Ok! Cleaning non-count errors!\n", f"0 Errors removed, {len(errors_to_clean)} to go!"]
        reply_message = await ctx.reply("```" + "\n".join(line for line in reply_text) + "```", mention_author=False)

        i = 0
        for error in errors_to_clean:
            message = await channel.fetch_message(int(error["message_id"]))
            await message.delete()
            i += 1
            reply_text[-1] = f"{i} Errors removed, {len(errors_to_clean) - i} to go!"
            await reply_message.edit(content="```" + "\n".join(line for line in reply_text) + "```")

        reply_text.append(f"\nDone! {i} errors removed!")
        await reply_message.edit(content="```" + "\n".join(line for line in reply_text) + "```")

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def update_tally(self, ctx: commands.Context) -> None:
        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        embed = discord.Embed()
        embed.title = "Count to 25,000 Tally Update"
        embed.description = "0 Messages Processed..."

        reply_message = await ctx.reply(embed=embed)

        table: dict[int, int] = {}
        messages_processed = 0
        async for message in channel.history(limit=None):
            if message.author.id in IDs.blacklist or convert_to_num(message) is None:
                continue

            table[message.author.id] = table.get(message.author.id, 0) + 1

            messages_processed += 1
            if messages_processed % 200 == 0:
                embed.description = f"{messages_processed} Messages Processed..."
                await reply_message.edit(embed=embed)

        embed.description = f"Finished processing {messages_processed} Messages"
        await reply_message.edit(embed=embed)

        for member in Member.members.values():
            member.counts = table.get(member.id, 0)
            member.write_data()

        embed.description += "\n\nDone!"
        await reply_message.edit(embed=embed)

    @commands.hybrid_command()
    async def tally(self, ctx: commands.Context) -> None:
        members = [member for member in Member.members.values() if member.counts > 0]
        members.sort(key=lambda m: m.counts, reverse=True)

        table = []
        last_counts = 25000
        rank = 0
        true_rank = 0
        for member in members:
            true_rank += 1
            if member.counts < last_counts:
                last_counts = member.counts
                rank = true_rank

            discord_user = self.bot.get_user(member.id)
            if discord_user is None:
                discord_user = await self.bot.fetch_user(member.id)

            table.append({
                "name": discord_user.display_name,
                "rank": rank,
                "counts": member.counts
            })

        output_text = "\n".join([f"{row['rank']}. {row['name']} - {row['counts']}" for row in table])

        embed = discord.Embed()
        embed.title = "Count to 25,000"
        embed.description = output_text

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def timeline(self, ctx: commands.Context) -> None:
        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        embed = discord.Embed()
        embed.title = "Count to 25,000 Timeline"
        embed.description = "0 Messages Processed..."

        reply_message = await ctx.reply(embed=embed)

        i = 0
        table: dict[date, int] = {}
        async for message in channel.history(limit=None, oldest_first=True):
            if convert_to_num(message) is not None:
                message_date = message.created_at.date()
                table[message_date] = table.get(message_date, 0) + 1

            i += 1
            if i % 200 == 0:
                embed.description = f"{i} Messages Processed..."
                await reply_message.edit(embed=embed)

        output_table: dict[str, list[str]] = {}
        for dt, counts in table.items():
            header = datetime.strftime(dt, "%B %Y")
            line = datetime.strftime(dt, "%A") + f" {humanize.ordinal(dt.day)} - {counts}"
            if header not in output_table:
                output_table[header] = []

            output_table[header].append(line)

        embed.clear_fields()
        for header, lines in output_table.items():
            embed.add_field(
                name=header,
                value="\n".join(lines)
            )

        for i, embed in enumerate(Utils.split_embeds(embed)):
            if i == 0:
                await reply_message.edit(embed=embed)
            else:
                await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def count_timeline(self, ctx: commands.Context):
        reply_message = await ctx.reply("Working on it!")
        channel = await self.bot.fetch_channel(925828116021121034)
        start_date = date(2021, 12, 29)
        end_date = date(2022, 12, 7)
        duration = (end_date - start_date).days + 1
        data_table: dict[int, list[int]] = {
            member.id: [0] * duration for member in Member.members.values()
        }

        i = 0
        async for message in channel.history(limit=None, before=discord.Object(1050179693925634100), oldest_first=True):
            if message.author.id in IDs.blacklist or convert_to_num(message) is None:
                continue
            d_index = (message.created_at.date() - start_date).days
            data_table[message.author.id][d_index] += 1
            i += 1
            if i % 200 == 0:
                await reply_message.edit(content=f"Processed {i} messages...")

        await reply_message.edit(content="Finished fetching messages!")

        to_del = []
        for member_id, count_list in data_table.items():
            if sum(count_list) == 0:
                to_del.append(member_id)
        for member_id in to_del:
            del data_table[member_id]

        for member_id, count_list in data_table.items():
            for i in range(1, duration):
                count_list[i] += count_list[i-1]

        headers = ["Member ID", "Avatar URL"] + [datetime.strftime(start_date + timedelta(days=i), "%x") for i in range(0, duration)]
        output_data = [",".join(headers)]

        for member_id, count_list in data_table.items():
            user = await self.bot.fetch_user(member_id)

            output_data.append(f"{user.display_name},{user.display_avatar.url}," + ",".join(str(n) for n in count_list))

        with open("data/live/bot/timeline.csv", "w+") as outfile:
            outfile.write("\n".join(line for line in output_data))

        with open("data/live/bot/timeline.csv", "rb") as infile:
            file = discord.File(infile)

        await reply_message.edit(content="Done", attachments=[file])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.channel.id != IDs.channels["Count"]:
            return
        if message.author.id in IDs.blacklist:
            return
        if convert_to_num(message) is None:
            return
        member = Member.get(message.author.id)

        count_correct = True
        last_count = await get_last_count(message)

        if last_count is not None:

            count_value = convert_to_num(message)
            last_count_value = convert_to_num(last_count)

            if message.author == last_count.author:
                count_correct = False
                await message.add_reaction("❗")

            if count_value != last_count_value + 1:
                count_correct = False
                await message.add_reaction("👀")

            if message.author.id in IDs.mods:
                last_member_count = await get_last_member_count(message)

                if last_member_count is not None:
                    offset = message.created_at.second + last_member_count.created_at.second
                    if message.created_at - last_member_count.created_at < timedelta(minutes=10, seconds=offset):
                        count_correct = False
                        await message.add_reaction("🕒")

        if count_correct:

            member.counts += 1
            member.balance += 1
            await member.xp.add(1, message)

            if member.counts == 1:
                lootpool = Lootpool.get("FirstCount")
            elif Item.currentEventBox is not None:
                if not member.collection.contains(Item.currentEventBox):
                    lootpool = Lootpool.get("EventBox")
                else:
                    lootpool = Lootpool.get("CountEvent")
            else:
                lootpool = Lootpool.get("Count")

            box = lootpool.roll()

            if box is not None:
                member.inventory.add(box)
                member.stats.countingBoxes += 1
                await message.reply(
                    f"Hey, would you look at that! You found a **{str(box)}**!",
                    mention_author=False
                )

            await member.missions.log_action_small("count", message)
            if member.collection.xp_value_changed:
                await member.xp.add(member.collection.commit_xp(), message)
        else:
            member.stats.incorrectCounts += 1

        member.write_data()

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.channel.id != IDs.channels["Count"]:
            return

        member = Member.get(before.author.id)

        reactions_list = [reaction.emoji for reaction in before.reactions]

        if "👀" in reactions_list and "🤩" not in reactions_list:
            last_count = await get_last_count(after)
            if convert_to_num(after) == convert_to_num(last_count) + 1:
                await after.add_reaction("🤩")

                member.write_data()


async def setup(bot):
    await bot.add_cog(Count(bot))
    print("Count Cog loaded")


async def teardown(bot):
    print("Count Cog unloaded")
    await bot.remove_cog(Count(bot))
