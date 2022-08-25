import discord
import random
import datetime
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


class Count(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def update_tally(self):
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()

        table = {}

        for member in Member.members.values():
            member.set_counts(0)

        for count in history:
            if convert_to_num(count) is None:
                continue

            table[count.author.id] = table.get(count.author.id, 0) + 1

        for authorid, counts in table.items():
            if authorid not in ids.blacklist:
                member = Member.get(authorid)
                member.set_counts(counts)

    @commands.command(brief="Shows the leaderboard of counts for the Count to 10,000.")
    async def tally(self, ctx):

        table = {}
        counts = 0

        for member in Member.members.values():
            if member.counts != 0:
                table[member.id] = member.counts
                counts += member.counts

        sortedTable = {}

        while len(table) > 0:
            currentMember = list(table.keys())[0]
            for member in table:
                if table[member] > table[currentMember]:
                    currentMember = member
            sortedTable[currentMember] = table[currentMember]
            table.pop(currentMember)

        tallyEmbed = discord.Embed(title="Count to 10,000", description=f"{counts} counts so far!", color=0xff5733)
        output = ""
        rank = 0
        displayRank = 0

        server = self.bot.get_guild(ids.server)

        lastScore = 10000
        for memberid, counts in sortedTable.items():
            rank += 1
            if counts < lastScore:
                displayRank = rank
                lastScore = counts

            member = server.get_member(memberid)
            if member is None:
                try:
                    member = await server.fetch_member(memberid)
                except discord.errors.NotFound:
                    member = None
            if member is None:
                memberName = "*Exorcised Shark*"
            else:
                memberName = f"{member.display_name}"

            if memberid == ctx.author.id:
                output += f"**{displayRank}: {memberName} - {counts}**\n"
            else:
                output += f"{displayRank}: {memberName} - {counts}\n"

        tallyEmbed.add_field(name="Leaderboard", value=output, inline=False)
        await ctx.send("Done! Here's the data!")
        await ctx.send(embed=tallyEmbed)

    @commands.command(brief="Shows the leaderboard of counts for the Count to 10,000.")
    async def full_tally(self, ctx):
        await ctx.send(
            "```Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes...```")
        await self.update_tally()
        await self.tally(ctx)

    @commands.command(brief="Shows the messages over time for the Count to 10,000.")
    async def timeline(self, ctx):
        await ctx.send(
            "Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
        table = {}
        for count in history:
            if count.author.id not in ids.blacklist:
                pass
            else:
                time = count.created_at
                timeString = str(time.day) + "/" + str(time.month)
                if timeString in table.keys():
                    table.update({timeString: table[timeString] + 1})
                else:
                    table[timeString] = 1
        history = []
        counts = 0
        arrayTable = []
        for timeString in table:
            arrayTable.insert(0, [timeString, table[timeString]])
            counts += table[timeString]
        table = {}

        tallyEmbed = discord.Embed(title="Count to 6969", description=f"{counts} counts so far!", color=0xff5733)
        output1 = ""
        output2 = ""
        output3 = ""
        total = 0
        for time in arrayTable:
            output1 = output1 + time[0] + "\n"
            output2 = output2 + str(time[1]) + "\n"
            total += time[1]
            output3 = output3 + str(total) + "\n"
        arrayTable = []

        tallyEmbed.add_field(name="Date   ", value=output1, inline=True)
        tallyEmbed.add_field(name="Counts", value=output2, inline=True)
        tallyEmbed.add_field(name="Total", value=output3, inline=True)

        await ctx.send("Done! Here's the data!")
        await ctx.send(embed=tallyEmbed)

    async def get_last_count(self, message, limit):
        messageHistory = await message.channel.history(limit=limit).flatten()
        flag = False
        for pastMessage in messageHistory:
            if not flag:
                if pastMessage.id == message.id:
                    flag = True
            else:
                if pastMessage.author.id not in ids.blacklist:
                    pastMessageValue = convert_to_num(pastMessage)
                    if pastMessageValue is not None:
                        return pastMessage, pastMessageValue

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == ids.channels["Count"] and message.author.id not in ids.blacklist:
            messageValue = convert_to_num(message)
            if messageValue is not None:
                countCorrect = True
                lastMessage, lastMessageValue = await self.get_last_count(message, 5)

                diff = 0
                while lastMessage.reactions:
                    lastMessage, lastMessageValue = await self.get_last_count(lastMessage, 5)
                    diff += 1

                if message.author.id == lastMessage.author.id:
                    countCorrect = False
                    await message.add_reaction("❗")

                if messageValue != lastMessageValue + diff + 1:
                    countCorrect = False
                    await message.add_reaction("👀")

                if message.author.id in ids.mods:
                    timeStart = message.created_at
                    timeStart = timeStart - datetime.timedelta(minutes=9, seconds=timeStart.second)
                    tenMinHistory = await message.channel.history(limit=20, after=timeStart).flatten()
                    foundMessage = discord.utils.get(tenMinHistory, author=message.author)
                    if foundMessage is not None and foundMessage != message:
                        countCorrect = False
                        await message.add_reaction("🕒")

                if countCorrect:
                    member = Member.get(message.author.id)
                    member.add_balance(1)
                    member.add_counts(1)

                    ##--Counting Boxes--##

                    box = None

                    ##----Event Box----##

                    if Item.currentEventBox is not None:
                        if Item.currentEventBoxID not in member.collection:
                            box = Item.currentEventBox

                    ##----Regular Box----##

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
                        member.add_to_inventory(box)
                        await message.reply(
                            f"Hey, would you look at that! You found a {box.rarity.get_icon(message.guild)} **{box.name}**!",
                            mention_author=False)
                    member.upload_data()

    @commands.Cog.listener()
    async def on_message_edit(self, oldMessage, message):
        if message.channel.id == ids.channels["Count"]:
            reactionsList = []
            for reaction in message.reactions:
                reactionsList.append(reaction.emoji)

            if '👀' in reactionsList:
                messageValue = convert_to_num(message)
                if messageValue is not None:
                    lastMessage, lastMessageValue = await self.get_last_count(message, 20)

                    if messageValue == lastMessageValue + 1:
                        await message.add_reaction("🤩")
                        member = Member.get(message.author.id)
                        member.add_counts(1)


async def setup(bot):
    await bot.add_cog(Count(bot))
    print("Count Cog loaded")


async def teardown(bot):
    print("Count Cog unloaded")
    await bot.remove_cog(Count(bot))
