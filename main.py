import discord
from discord.ext import tasks, commands

import sys
import os
import datetime

import secret

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)

if secret.testBot:
    import testids as ids
else:
    import ids


@bot.event
async def on_ready():
    print(f"\nSharkbot ready on {bot.user} : {bot.user.id}")
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
        print(f"-{guild.name} : {guild.id}")
        print(f"--Members: {len(guild.members)}")
        print(f"--Text Channels: {len(guild.text_channels)}")
        print(f"--Voice Channels: {len(guild.voice_channels)}")


@bot.command()
@commands.check_any(commands.is_owner())
async def reboot(ctx):
    await ctx.send("Alright! Rebooting now!")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))

    f = open("reboot.txt", "w")
    f.write("True " + str(ctx.channel.id))
    f.close()

    os.system("sudo reboot")


@bot.command()
@commands.check_any(commands.is_owner())
async def load(message, extension):
    bot.load_extension(f"cogs.{extension.lower()}")
    await message.channel.send(f"{extension.capitalize()} loaded.")


@bot.command()
@commands.check_any(commands.is_owner())
async def unload(message, extension):
    bot.unload_extension(f"cogs.{extension.lower()}")
    await message.channel.send(f"{extension.capitalize()} unloaded.")


@bot.command()
@commands.check_any(commands.is_owner())
async def reload(ctx, extension="all"):
    extension = extension.lower()

    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                ext = filename[:-3]
                bot.unload_extension(f"cogs.{ext}")
                bot.load_extension(f"cogs.{ext}")
                await ctx.send(f"{ext.capitalize()} reloaded.")
                print(f"{ext.capitalize()} Cog reloaded.")
    else:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension.capitalize()} reloaded.")
        print(f"{extension.capitalize()} Cog reloaded.")


@bot.command()
@commands.check_any(commands.is_owner())
async def rebuild(ctx, extension="all"):
    await ctx.invoke(bot.get_command("pull"))
    await ctx.invoke(bot.get_command("reload"), extension=extension)


@bot.command()
@commands.check_any(commands.is_owner())
async def pull(ctx):
    os.system("git pull")
    await ctx.send("Pulling latest commits.")


@bot.command()
@commands.check_any(commands.is_owner())
async def checkout(ctx, branch):
    os.system(f"git checkout {branch}")
    await ctx.send(f"Switched to {branch} branch.")
    os.system("git pull")
    await ctx.send("Pulling latest commits.")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(secret.token)
