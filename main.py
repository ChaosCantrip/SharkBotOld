import discord
from discord.ext import commands
import secret
import os
import datetime

if secret.testBot:
    import testids as ids
else:
    import ids

bot = commands.Bot("$")


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

def check_for_role(member, roleid):
    for role in member.roles:
        if role.id == roleid:
            return True
    return False

@bot.event
async def on_ready():
    print(f"Sharkbot ready on {bot.user} : {bot.user.id}")
    chaos = await bot.fetch_user(220204098572517376)
    await chaos.send("SharkBot is up and running!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="nom nom nom!"))

    print("")
    print("The bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"{guild.name} : {guild.id}")



@bot.command()
async def tally(message):
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

    arrayTable = []
    for author in table:
        if author.id != ids.users["MEE6"]:
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



@bot.command()
async def reboot(message):
    if message.author.id != ids.users["Chaos"]:
        await message.channel.send("I'm afraid you're not allowed to do that!")
    else:
        await message.channel.send("Alright! Rebooting now!")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))

        os.system("sudo reboot")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id in ids.blacklist:
        return

    if message.channel.id == ids.channels["Count"]:
        
        messages = await message.channel.history(limit=3).flatten()
        if messages[1].author.id == ids.users["MEE6"]:
            prev_message = convert_to_num(messages[2])
        else:
            prev_message = convert_to_num(messages[1])
        if convert_to_num(message) != prev_message + 1:
            await message.add_reaction("\N{EYES}")

        authorMention = "<@!" + str(message.author.id) + ">"

        if (authorMention in split_into_messages(await bot.get_channel(ids.channels["People who count"]).history().flatten())) == False:

            await bot.get_channel(ids.channels["People who count"]).send(authorMention)

        if check_for_role(message.author, ids.roles["Mod"]) or check_for_role(message.author, ids.roles["Admin"]):
            hist = await bot.get_channel(ids.channels["Count"]).history(limit=20).flatten()
            for mes in hist[1:]:
                if mes.author == message.author:
                    seconds = (message.created_at - mes.created_at).total_seconds()
                    if seconds < 540:
                        await message.author.send("Naughty Naughty!")
                        await message.add_reaction("\N{EYES}")
                    break

    await bot.process_commands(message)



bot.run(secret.token)
