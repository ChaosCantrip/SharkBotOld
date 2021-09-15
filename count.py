import discord
import secret

if secret.testBot:
    import testids as ids
else:
    import ids


def convert_to_num(message):

    result = ""

    for num in message.content:
        if num.isdigit():
            result = result + num

    if(result == ""):
        return 0
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



async def check_correct_number(message):
        
    prev_message = await message.channel.history(limit=5).find(lambda m: m.author != message.author and m.author.id not in ids.blacklist)
    if convert_to_num(message) == convert_to_num(prev_message) + 1:
        return True
    else:
        return False



async def update_list(bot, message):

    authorMention = "<@!" + str(message.author.id) + ">"

    listChannel = bot.get_channel(ids.channels["People who count"])

    messageList = []
    for listMessage in await listChannel.history().flatten():
        messageList.append(listMessage.content)

    if authorMention not in messageList:
        await listChannel.send(authorMention)



async def check_admin_slowmode(message, cooldownTime):
    hist = await message.channel.history(limit=20).flatten()
    for msg in hist[1:]:
        if msg.author == message.author:
            return (message.created_at - msg.created_at).total_seconds() < cooldownTime



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
    counts = len(history)
    history = []

    arrayTable = []
    for author in table:
        if author.id != ids.users["MEE6"]:
            arrayTable.append([author.display_name, table[author]])
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

