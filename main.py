import discord
import secret
import os

client = discord.Client()

def convert_to_num(message):

    result = ""

    for num in message.content:
        if num.isdigit():
            result = result + num

    if(result == ""):
        return 0
    else:
        return int(result)


def split_into_messages(history):
    result = []
    for message in history:
        result.append(message.content)
    return result

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

@client.event
async def on_ready():
    print("ChaosShark Bot ready as {0.user}".format(client))
    chaos = await client.fetch_user(220204098572517376)
    await chaos.send("SharkBot is up and running!")

@client.event
async def on_message(message):

    shark = await client.fetch_guild(681947994093912087)

    if shark.get_role(776196526846246922) in message.author.roles:
        print("sus")
        return 

    print(message.author.roles)

    if message.content == "$go away":
        await message.guild.leave()
    
    if message.content == "$reboot":
        await message.channel.send("Alright! Rebooting now!")
        os.system("sudo reboot")

    if message.content == "$tally":
        await message.channel.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
        history = await client.get_channel(885239863023136788).history(limit=None).flatten()
        table = {}
        for count in history:
            author = count.author
            if author in table.keys():
                table.update({author : table[author] + 1})
            else:
                table[author] = 1
        history = []

        arrayTable = []
        for author in table:
            if author.id != 159985870458322944:
                arrayTable.append([author.display_name, table[author]])
        table = {}

        sortedTable = sort_tally_table(arrayTable)
        arrayTable = []
        
        output = ""
        for author in sortedTable:
                output = output + author[0] + " - " + str(author[1]) + "\n"
        sortedTable = []

        await message.channel.send("Done! Here's the data!")
        await message.channel.send("```" + output + "```")


    if message.channel.id == 885239863023136788:
        
        messages = await message.channel.history(limit=2).flatten()
        if convert_to_num(message) != convert_to_num(messages[1]) + 1:
            await message.add_reaction("\N{NEUTRAL FACE}")

        authorAt = "<@!" + str(message.author.id) + ">"

        if (authorAt in split_into_messages(await client.get_channel(885915443506868264).history().flatten())) == False:

            await client.get_channel(885915443506868264).send(authorAt)

            
client.run(secret.token)
