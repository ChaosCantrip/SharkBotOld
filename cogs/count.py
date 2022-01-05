import discord
from discord.ext import commands

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

    if(result == ""):
        return None
    else:
        return int(result)



def sort_tally_table(table):
    n = len(table)

    for i in range(n):
        already_sorted = True

        for j in range (n - i - 1):
            if table[j][1] < table[j+1][1]:
                table[j], table[j+1] = table[j+1], table[j]
                already_sorted = False
        if already_sorted:
            break
    return table



class Count(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        


    async def check_list(self, message):
    
        countChannel = self.bot.get_channel(ids.channels["Count"])
        listChannel = self.bot.get_channel(ids.channels["People who count"])
    
        allCounts = await countChannel.history(limit=None).flatten()
        counters = []
    
        for counter in await listChannel.history(limit=None).flatten():
            counters.append(counter.content)
    
        for count in allCounts:
            authorMention = "<@!" + str(count.author.id) + ">"
            if count.author.id not in ids.blacklist and authorMention not in counters:
                counters.append(authorMention)
                await listChannel.send(authorMention)
   
    async def update_list(self, message):

        authorMention = "<@!" + str(message.author.id) + ">"

        listChannel = self.bot.get_channel(ids.channels["People who count"])

        messageList = []
        for listMessage in await listChannel.history().flatten():
            messageList.append(listMessage.content)

        if authorMention not in messageList:
            await listChannel.send(authorMention)


    
    @commands.command()
    async def tally(self, message):
        await message.channel.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
        table = {}
        for count in reversed(history):
            if convert_to_num(count) == None:
                continue
            author = count.author
            if author in table.keys():
                table.update({author : table[author] + 1})
            else:
                table[author] = 1
        history = []
        counts = 0
        arrayTable = []
        for author in table:
            if author.id not in ids.blacklist:
                arrayTable.append([author.display_name, table[author]])
                counts += table[author]
        table = {}

        sortedTable = sort_tally_table(arrayTable)
        arrayTable = []

        tallyEmbed=discord.Embed(title="Count to 10,000", description=f"{counts} counts so far!", color=0xff5733)
        output = ""
        rank = 0
        displayRank = 0

        lastScore = 10000
        for author in sortedTable:
            rank += 1
            if author[1] < lastScore:
                displayRank = rank
                lastScore = author[1]
            output = output + f"{displayRank}: {author[0]} - {author[1]} \n"
        sortedTable = []

        tallyEmbed.add_field(name="Leaderboard", value=output, inline=False)

        await message.channel.send("Done! Here's the data!")
        await message.channel.send(embed=tallyEmbed)


def setup(bot):
    bot.add_cog(Count(bot))