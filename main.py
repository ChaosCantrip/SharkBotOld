import discord
from discord.ext import commands

import sys
import os
import datetime

import secret



bot = commands.Bot("$")



import count
if secret.testBot:
    import testids as ids
else:
    import ids

    
@bot.command()
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
async def load(message, extension):
    bot.load_extension(f"cogs.{extension}")
    print(f"{extension} loaded.")


    
@bot.command()
async def unload(message, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"{extension} unloaded.")


    
@bot.command()
async def reload(message, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"{extension} unloaded.")
    bot.load_extension(f"cogs.{extension}")
    print(f"{extension} loaded.")
    print(f"{extension} reloaded.")



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(secret.token)
