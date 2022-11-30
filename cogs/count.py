import random
from datetime import datetime, timedelta
from typing import Union

import discord
from discord.ext import commands

from SharkBot import Member, Item, IDs, Lootpool


def convert_to_num(message):
    result = ""

    for char in message.content:
        if char.isdigit():
            result = result + char

    if result == "":
        return None
    else:
        return int(result)


async def get_last_count(message) -> Union[discord.Message, None]:
    found = False
    async for pastMessage in message.channel.history(limit=None):
        if not found:
            found = pastMessage.id == message.id
        else:
            if pastMessage.author.id in IDs.blacklist or convert_to_num(pastMessage) is None:
                continue
            return pastMessage
    return None


async def get_last_member_count(message) -> Union[discord.Message, None]:
    found = False
    async for pastMessage in message.channel.history(limit=None):
        if not found:
            found = pastMessage.id == message.id
        else:
            if pastMessage.author.id is not message.author.id:
                continue
            return pastMessage
    return None


class Count(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def updatetally(self, ctx: commands.Context) -> None:
        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        output_text = "Working on it!"
        message = await ctx.send(f"```{output_text}```")
        output_text += "\n"

        for member in Member.members.values():
            member.counts = 0

        progress = 0
        async for pastMessage in channel.history(limit=None):
            progress += 1
            if progress % 200 == 0:
                output_text += f"\n{progress} messages processed..."
                await message.edit(content=f"```{output_text}```")

            if pastMessage.author.id in IDs.blacklist:
                continue
            if convert_to_num(pastMessage) is None:
                continue

            member = Member.get(pastMessage.author.id)
            member.counts += 1

        for member in Member.members.values():
            member.write_data()

        output_text += "\n\nDone!"
        await message.edit(content=f"```{output_text}```")

        await self.tally(ctx)

    @commands.hybrid_command()
    async def tally(self, ctx: commands.Context) -> None:
        server = await self.bot.fetch_guild(IDs.servers["Shark Exorcist"])
        member_names = {member.id: member.display_name async for member in server.fetch_members()}

        members = [member for member in Member.members.values() if member.counts > 0]
        members.sort(key=lambda m: m.counts, reverse=True)

        table = []
        last_counts = 10000
        rank = 0
        true_rank = 0
        for member in members:
            true_rank += 1
            if member.counts < last_counts:
                last_counts = member.counts
                rank = true_rank

            member_name = member_names[member.id] if member.id in member_names else "*Exorcised Shark*"

            table.append({
                "name": member_name,
                "rank": rank,
                "counts": member.counts
            })

        output_text = "\n".join([f"{row['rank']}. {row['name']} - {row['counts']}" for row in table])

        embed = discord.Embed()
        embed.title = "Count to 10,000"
        embed.description = output_text

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def timeline(self, ctx: commands.Context) -> None:
        channel = await self.bot.fetch_channel(IDs.channels["Count"])

        output_text = "Working on it!"
        message = await ctx.send(f"```{output_text}```")
        output_text += "\n"

        table = {}
        progress = 0
        async for pastMessage in channel.history(limit=None, oldest_first=True):
            progress += 1
            if progress % 200 == 0:
                output_text += f"\n{progress} messages processed..."
                await message.edit(content=f"```{output_text}```")

            date = datetime.strftime(pastMessage.created_at, "%d/%m/%Y")
            table[date] = table.get(date, 0) + 1

        result_text = "\n".join([f"{date} - {counts}" for date, counts in table.items()])

        embed = discord.Embed()
        embed.title = "Timeline"
        embed.description = result_text

        await message.edit(content=None, embed=embed)

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
        last_member_count = await get_last_member_count(message)

        if last_count is not None:

            count_value = convert_to_num(message)
            last_count_value = convert_to_num(last_count)

            if message.author == last_count.author:
                count_correct = False
                await message.add_reaction("❗")

            if count_value != last_count_value + 1:
                count_correct = False
                await message.add_reaction("👀")

            if last_member_count is not None:

                if message.created_at - last_member_count.created_at < timedelta(minutes=10):
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
                    f"Hey, would you look at that! You found a {box.rarity.icon} **{box.name}**!",
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
