import discord
from discord.ext import commands

import sys
import os
import datetime

import secret



bot = commands.Bot("$")



if secret.testBot:
    import testids as ids
else:
    import ids



@bot.event
async def on_ready():
    print(f"Sharkbot ready on {bot.user} : {bot.user.id}")
    chaos = await bot.fetch_user(ids.users["Chaos"])    
    
    await chaos.send("SharkBot is up and running!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="nom nom nom!"))
    
    r = open("reboot.txt", "r")
    replyTxt = r.read()
    replyFlag, replyID = replyTxt.split()
    r.close()
    
    if replyFlag == "True":
        replyChannel = await bot.fetch_channel(int(replyID))
        await replyChannel.send("I'm back!")
        w = open("reboot.txt", "w")
        w.write(f"False {replyID}")
        w.close()
    
    print("")
    print("The bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"{guild.name} : {guild.id}")



@bot.command()
@commands.check_any(commands.is_owner())
async def reboot(message):
    if message.author.id != ids.users["Chaos"]:
        await message.channel.send("I'm afraid you're not allowed to do that!")
    else:
        await message.channel.send("Alright! Rebooting now!")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))
        
        f = open("reboot.txt", "w")
        f.write("True " + str(message.channel.id))
        f.close()

        os.system("sudo reboot")



@bot.command()
@commands.check_any(commands.is_owner())
async def load(message, extension):
    bot.load_extension(f"cogs.{extension}")
    await message.channel.send(f"{extension} loaded.")
    print(f"{extension} loaded.")


    
@bot.command()
@commands.check_any(commands.is_owner())
async def unload(message, extension):
    bot.unload_extension(f"cogs.{extension}")
    await message.channel.send(f"{extension} unloaded.")
    print(f"{extension} unloaded.")


    
@bot.command()
@commands.check_any(commands.is_owner())
async def reload(message, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"{extension} unloaded.")
    bot.load_extension(f"cogs.{extension}")
    print(f"{extension} loaded.")
    await message.channel.send(f"{extension} reloaded.")
    print(f"{extension} reloaded.")

@bot.command()
@commands.check_any(commands.is_owner())
async def pull(message):
    os.system("git pull")



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(secret.token)
