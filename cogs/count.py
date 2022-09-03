from typing import Union

import discord
import random
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from definitions import Member, Item

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


def convert_to_num(message):
    result = ""

    for char in message.content:
        if char.isdigit():
            result = result + char

    if result == "":
        return None
    else:
        return int(result)


async def get_last_count(message, limit=10) -> Union[discord.Message, None]:
    found = False
    async for pastMessage in message.channel.history(limit=limit):
        if not found:
            found = pastMessage.id == message.id
        else:
            if pastMessage.author.id in ids.blacklist or convert_to_num(pastMessage) is None:
                continue
            return pastMessage
    return None


class Count(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def updatetally(self, ctx: commands.Context) -> None:
        channel = await self.bot.fetch_channel(ids.channels["Count"])

        outputText = "Working on it!"
        message = await ctx.send(f"```{outputText}```")
        outputText += "\n"

        for member in Member.members.values():
            member.set_counts(0)

        progress = 0
        async for pastMessage in channel.history(limit=None):
            progress += 1
            if progress % 200 == 0:
                outputText += f"\n{progress} messages processed..."
                await message.edit(content=f"```{outputText}```")

            if pastMessage.author.id in ids.blacklist:
                continue
            if convert_to_num(pastMessage) is None:
                continue

            member = Member.get(pastMessage.author.id)
            member.add_counts(1)

        outputText += "\n\nDone!"
        await message.edit(content=f"```{outputText}```")

        await self.tally(ctx)

    @commands.hybrid_command()
    async def tally(self, ctx: commands.Context) -> None:
        server = await self.bot.fetch_guild(ids.server)
        memberNames = {member.id: member.display_name async for member in server.fetch_members()}

        members = [member for member in Member.members.values() if member.counts > 0]
        members.sort(key=lambda m: m.get_counts(), reverse=True)

        table = []
        lastCounts = 10000
        rank = 0
        trueRank = 0
        for member in members:
            trueRank += 1
            if member.get_counts() < lastCounts:
                lastCounts = member.get_counts()
                rank = trueRank

            memberName = memberNames[member.id] if member.id in memberNames else "*Exorcised Shark*"

            table.append({
                "name": memberName,
                "rank": rank,
                "counts": member.get_counts()
            })

        outputText = "\n".join([f"{row['rank']}. {row['name']} - {row['counts']}" for row in table])

        embed = discord.Embed()
        embed.title = "Count to 10,000"
        embed.description = outputText

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def timeline(self, ctx: commands.Context) -> None:
        channel = await self.bot.fetch_channel(ids.channels["Count"])

        outputText = "Working on it!"
        message = await ctx.send(f"```{outputText}```")
        outputText += "\n"

        table = {}
        progress = 0
        async for pastMessage in channel.history(limit=None, oldest_first=True):
            progress += 1
            if progress % 200 == 0:
                outputText += f"\n{progress} messages processed..."
                await message.edit(content=f"```{outputText}```")

            date = datetime.strftime(pastMessage.created_at, "%d/%m/%Y")
            table[date] = table.get(date, 0) + 1

        resultText = "\n".join([f"{date} - {counts}" for date, counts in table.items()])

        embed = discord.Embed()
        embed.title = "Timeline"
        embed.description = resultText

        await message.edit(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.channel.id != ids.channels["Count"]:
            return
        if message.author.id in ids.blacklist:
            return
        if convert_to_num(message) is None:
            return

        countCorrect = True
        lastCount = await get_last_count(message)
        if lastCount is not None:
            countValue = convert_to_num(message)
            lastCountValue = convert_to_num(lastCount)

            if message.author == lastCount.author:
                countCorrect = False
                await message.add_reaction("❗")

            # if message.created_at - lastCount.created_at < timedelta(minutes=10):
            #     countCorrect = False
            #     await message.add_reaction("🕒")

            if countValue != lastCountValue + 1:
                countCorrect = False
                await message.add_reaction("👀")

        if countCorrect:
            member = Member.get(message.author.id)

            member.add_counts(1)
            member.add_balance(1)
            member.missions.log_action("count")

            box = None

            if Item.currentEventBox is not None and not member.collection.contains(Item.currentEventBox):
                box = Item.currentEventBox

            if box is None:
                if random.randint(1, 8) == 8:
                    roll = random.randint(1, 100)
                    if roll < 3:
                        box = Item.get("LOOT5")
                    elif roll < 10:
                        box = Item.get("LOOT4")
                    elif roll < 25:
                        box = Item.get("LOOT3")
                    elif roll < 50:
                        box = Item.get("LOOT2")
                    else:
                        box = Item.get("LOOT1")

            if box is not None:
                member.inventory.add(box)
                await message.reply(
                    f"Hey, would you look at that! You found a {box.rarity.icon} **{box.name}**!",
                    mention_author=False
                )

            member.write_data()
            member.upload_data()

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.channel.id != ids.channels["Count"]:
            return

        reactionsList = [reaction.emoji for reaction in before.reactions]

        if "👀" in reactionsList and "🤩" not in reactionsList:
            lastCount = await get_last_count(after)
            if convert_to_num(after) == convert_to_num(lastCount) + 1:
                await after.add_reaction("🤩")


async def setup(bot):
    await bot.add_cog(Count(bot))
    print("Count Cog loaded")


async def teardown(bot):
    print("Count Cog unloaded")
    await bot.remove_cog(Count(bot))
