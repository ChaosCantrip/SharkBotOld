import discord
import secret
import datetime

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



def split_into_messages(history):
    result = []
    for message in history:
        result.append(message.content)
    return result


async def check_list(bot):
    
    countChannel = bot.get_channel(ids.channels["Count"])
    listChannel = bot.get_channel(ids.channels["People who count"])
    
    allCounts = await countChannel.history(limit=None).flatten()
    counters = []
    
    for counter in await listChannel.history(limit=None).flatten():
        counters.append(counter.content)
    
    for count in allCounts:
        authorMention = "<@!" + str(count.author.id) + ">"
        if count.author.id not in ids.blacklist and authorMention not in counters:
            counters.append(authorMention)
            await listChannel.send(authorMention)

async def update_list(bot, message):

    authorMention = "<@!" + str(message.author.id) + ">"

    listChannel = bot.get_channel(ids.channels["People who count"])

    messageList = []
    for listMessage in await listChannel.history().flatten():
        messageList.append(listMessage.content)

    if authorMention not in messageList:
        await listChannel.send(authorMention)


async def tally_channel(bot, message, chan):
    await message.channel.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
    chanl = await bot.fetch_channel(chan)
    history = await chanl.history(limit=None).flatten()
    table = {}
    for count in history:
        author = count.author
        if author in table.keys():
            table.update({author : table[author] + 1})
        else:
            table[author] = 1
    history = []
    counts = 0
    arrayTable = []
    for author in table:
        if author.id != ids.users["MEE6"]:
            arrayTable.append([author.display_name, table[author]])
            counts += table[author]
    table = {}

    sortedTable = sort_tally_table(arrayTable)
    arrayTable = []

    tallyEmbed=discord.Embed(title=chanl.name, description=f"{counts} messages so far!", color=0xff5733)
    output = ""
    for author in sortedTable:
            output = output + author[0] + " - " + str(author[1]) + "\n"
    sortedTable = []

    tallyEmbed.add_field(name="Leaderboard", value=output, inline=False)

    await message.channel.send("Done! Here's the data!")
    await message.channel.send(embed=tallyEmbed)

async def verify_count(bot, message):
    await message.channel.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
    history = await bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
    history.reverse()
    currentNum = 0
    for msg in history:
        if msg.author.id not in ids.blacklist:
            if convert_to_num(msg) != currentNum + 1:
                await message.channel.send(msg.author.display_name + msg.content)
            currentNum += 1
    await message.channel.send("Done!")





async def tally(bot, message):
    await message.channel.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
    history = await bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
    table = {}
    for count in history:
        author = count.author
        if author in table.keys():
            table.update({author : table[author] + 1})
        else:
            table[author] = 1
    history = []
    counts = 0
    arrayTable = []
    for author in table:
        if author.id != ids.users["MEE6"]:
            arrayTable.append([author.display_name, table[author]])
            counts += table[author]
    table = {}

    sortedTable = sort_tally_table(arrayTable)
    arrayTable = []

    tallyEmbed=discord.Embed(title="Count to 6969", description=f"{counts} counts so far!", color=0xff5733)
    output = ""
    for author in sortedTable:
            output = output + author[0] + " - " + str(author[1]) + "\n"
    sortedTable = []

    tallyEmbed.add_field(name="Leaderboard", value=output, inline=False)

    await message.channel.send("Done! Here's the data!")
    await message.channel.send(embed=tallyEmbed)


    
async def timeline(bot, message):
    await message.channel.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
    history = await bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
    table = {}
    for count in history:
        if count.author.id == ids.users["MEE6"]:
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

    await message.channel.send("Done! Here's the data!")
    await message.channel.send(embed=tallyEmbed)



async def get_last_count(bot, message, limit):
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


async def process_message(bot, message):
    messageValue = convert_to_num(message)
    if messageValue != None:
        lastMessage, lastMessageValue = await get_last_count(bot, message, 10)

        if message.author.id == lastMessage.author.id:
            await message.add_reaction("❗")

        if messageValue != lastMessageValue + 1:
            await message.add_reaction("👀")

        await update_list(bot, message)



async def verify_message_edit(bot, message):
    reactionsList = []
    for reaction in message.reactions:
        reactionsList.append(reaction.emoji)

    if '👀' in reactionsList:
        print(True)
        messageValue = convert_to_num(message)
        if messageValue != None:
            lastMessage, lastMessageValue = await get_last_count(bot, message, 20)

            if messageValue == lastMessageValue + 1:
                await message.add_reaction("🤩")




        

