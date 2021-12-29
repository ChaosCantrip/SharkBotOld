import discord
import sys
from discord.ext import commands
import secret
import os
import datetime
import count

if secret.testBot:
    import testids as ids
else:
    import ids

bot = commands.Bot("$")



async def report_error(message, error):
    chaos = await bot.fetch_user(ids.users["Chaos"])
    report = f"ERROR REPORT \nRaised by:\n{message.author.name} : {message.author.id}\n"
    if message.guild != None:
        report = report + f"in {message.guild.name}, {message.channel.name} : {message.guild.id}, {message.channel.id}"
    else:
        report = report + "in DMs"
    report = report + f"\nMessage ID: {message.id} \nMessage Text: {message.content} \n \nError:\n"
    
    for note in sys.exc_info():
        report = report + str(note) + "\n"
    await chaos.send("```" + report + "```")

    
    
@bot.event
async def on_ready():
    print(f"Sharkbot ready on {bot.user} : {bot.user.id}")
    chaos = await bot.fetch_user(220204098572517376)    
    
    await chaos.send("SharkBot is up and running!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="nom nom nom!"))
    await count.check_list(bot)
    
    r = open("reboot.txt", "r")
    replyID = r.read()
    replyChannel = await bot.fetch_channel(int(replyID))
    await replyChannel.send("I'm back")
    r.close()
    print("")
    print("The bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"{guild.name} : {guild.id}")

        
        
@bot.command()
async def verify(message):
    await count.verify_count(bot, message)

    
    
@bot.command()
async def tally(message):
    await count.tally(bot, message)


    
@bot.command()
async def tallychannel(message, arg):
    if message.author.id in [ids.users["Luke"], ids.users["Chaos"], ids.users["HxRL"]]:
        await count.tally_channel(bot, message, int(arg)) 


        
@bot.command()
async def timeline(message):
    await count.timeline(bot, message)


    
@bot.command()
async def reboot(message):
    if message.author.id != ids.users["Chaos"]:
        await message.channel.send("I'm afraid you're not allowed to do that!")
    else:
        await message.channel.send("Alright! Rebooting now!")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))
        
        f = open("reboot.txt", "w")
        f.write(str(message.channel.id))
        f.close()

        os.system("sudo reboot")



@bot.command()
async def ping(message):
    await message.channel.send("Pong!")


    
@bot.event
async def on_message(message):
    try:
        await process_message(message)
    except Exception as e:
        await report_error(message, e)

        
        
@bot.event
async def on_message_edit(oldMessage, newMessage):
    try:
        await count.verify_message_edit(bot, newMessage)
    except Exception as e:
        await report_error(newMessage, e)

async def process_message(message):
        if message.author == bot.user:
            return

        if message.author.id in ids.blacklist:
            return

        if message.channel.id == ids.channels["Count"]:
            await count.process_message(bot, message)


        await bot.process_commands(message)


        
bot.run(secret.token)
