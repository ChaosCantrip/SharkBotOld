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
        


    async def check_list(self):
    
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
   


    async def update_list(self, count):

        authorMention = "<@!" + str(count.author.id) + ">"

        listChannel = self.bot.get_channel(ids.channels["People who count"])

        messageList = []
        for listMessage in await listChannel.history().flatten():
            messageList.append(listMessage.content)

        if authorMention not in messageList:
            await listChannel.send(authorMention)



    async def read_tally_file(self):
        r = open("tally.txt", "r")
        fileData = r.readlines()
        r.close()
        lastCount = int(fileData[0])
        tallyData = {}
        for line in fileData[1:]:
            lineData = line.split(":")
            tallyData[int(lineData[0])] = int(lineData[1])
        return lastCount, tallyData



    async def write_tally_data(self, lastCount, tallyData):
        fileData = str(lastCount)
        for line in tallyData:
            if line not in ids.blacklist:
                fileData += f"\n{line}:{tallyData[line]}"
        w = open("tally.txt", "w")
        w.write(fileData)
        w.close()
           


    async def get_latest_count(self):
        messageHistory = await self.bot.get_channel(ids.channels["Count"]).history(limit=5).flatten()
        for pastMessage in messageHistory:
            if pastMessage.author.id not in ids.blacklist:
                pastMessageValue = convert_to_num(pastMessage)
                if pastMessageValue != None:
                    return pastMessage, pastMessageValue
        return message, messageValue



    async def full_tally(self):
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
        tallyData = {}
        for count in reversed(history):
            if convert_to_num(count) == None:
                continue
            authorId = count.author.id
            if authorId in tallyData.keys():
                tallyData.update({authorId : tallyData[authorId] + 1})
            else:
                tallyData[authorId] = 1
        latestCount, latestCountValue = await self.get_latest_count()
        await self.write_tally_data(latestCountValue, tallyData)



    async def update_tally(self):
        lastDataValue, tallyData = await self.read_tally_file()
        lastCount, lastCountValue = await self.get_latest_count()
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=(lastCountValue - lastDataValue + 10)).flatten()
        for count in reversed(history):
            countValue = convert_to_num(count)
            if countValue == None:
                continue
            if countValue > lastDataValue:
                if count.author.id in tallyData.keys():
                    tallyData.update({count.author.id : tallyData[count.author.id] + 1})
                else:
                    tallyData[count.author.id] = 1
        latestCount, latestCountValue = await self.get_latest_count()
        await self.write_tally_data(latestCountValue, tallyData)


    async def generate_tally_embed(self):
        lastDataValue, tallyData = await self.read_tally_file()
        counts = 0
        arrayTable = []
        shark = await self.bot.fetch_guild(ids.server)
        for authorId in tallyData:
            author = await shark.fetch_member(authorId)
            arrayTable.append([author.display_name, tallyData[authorId]])
            counts += tallyData[authorId]

        sortedTable = sort_tally_table(arrayTable)
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

        tallyEmbed=discord.Embed(title="Count to 10,000", description=f"{counts} counts so far!", color=0xff5733)
        tallyEmbed.add_field(name="Leaderboard", value=f"{output}", inline=False)

        return tallyEmbed


    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def fullTally(self, ctx):
        await self.full_tally()
        tallyEmbed = await self.generate_tally_embed()
        await ctx.send(embed=tallyEmbed)



    
    @commands.command(brief="Shows the leaderboard of counts for the Count to 10,000.")
    async def tally(self, ctx):
        await self.update_tally()
        tallyEmbed = await self.generate_tally_embed()
        await ctx.send(embed=tallyEmbed)

    
        
    @commands.command(brief="Shows the messages over time for the Count to 10,000.")
    async def timeline(self, ctx):
        await ctx.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
        table = {}
        for count in history:
            if count.author.id not in ids.blacklist:
                pass
            else:
                time = count.created_at
                timeString = str(time.day) + "/" + str(time.month)
                if timeString in table.keys():
                    table.update({timeString : table[timeString] + 1})
                else:
                    table[timeString] = 1
        history = []
        counts = 0
        arrayTable = []
        for timeString in table:
            arrayTable.insert(0, [timeString, table[timeString]])
            counts += table[timeString]
        table = {}

        tallyEmbed=discord.Embed(title="Count to 6969", description=f"{counts} counts so far!", color=0xff5733)
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



    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_list()


        
    async def get_previous_count(self, message, limit):
        messageHistory = await message.channel.history(limit=limit).flatten()
        flag = False
        for pastMessage in messageHistory:
            if flag == False:
                if pastMessage.id == message.id:
                    flag = True
            else:
                if pastMessage.author.id not in ids.blacklist:
                    pastMessageValue = convert_to_num(pastMessage)
                    if pastMessageValue != None:
                        return pastMessage, pastMessageValue
        return message, messageValue



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == ids.channels["Count"] and message.author.id not in ids.blacklist:
            messageValue = convert_to_num(message)
            if messageValue != None:
                lastMessage, lastMessageValue = await self.get_previous_count(message, 10)

                if message.author.id == lastMessage.author.id:
                    await message.add_reaction("❗")

                if messageValue != lastMessageValue + 1:
                    await message.add_reaction("👀")

                await self.update_list(message)



    @commands.Cog.listener()
    async def on_message_edit(self, oldMessage, message):
        if message.channel.id == ids.channels["Count"]:
            reactionsList = []
            for reaction in message.reactions:
                reactionsList.append(reaction.emoji)

            if '👀' in reactionsList:
                messageValue = convert_to_num(message)
                if messageValue != None:
                    lastMessage, lastMessageValue = await self.get_previous_count(message, 20)

                    if messageValue == lastMessageValue + 1:
                        await message.add_reaction("🤩")



def setup(bot):
    bot.add_cog(Count(bot))
    print("Count Cog loaded")

def teardown(bot):
    print("Count Cog unloaded")
    bot.remove_cog(Count(bot))
