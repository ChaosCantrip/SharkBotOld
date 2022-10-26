import asyncio
import os
from datetime import datetime
import sys

import aiohttp
import discord
from discord.ext import commands

import secret
import SharkBot

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print("\nSharkBot connected to Discord")
    print(f"- Account: {bot.user}")
    print(f"- User ID: {bot.user.id}")

    if not os.path.exists("data/live/bot/lastmessage.txt"):
        lastTime = None
    else:
        with open("data/live/bot/lastmessage.txt", "r") as infile:
            lastTime = datetime.strptime(infile.read(), "%d/%m/%Y-%H:%M:%S:%f")

    embed = discord.Embed()
    embed.title = "SharkBot is up and running!"
    embed.description = f"<t:{int(datetime.now().timestamp())}:F>"

    with open("data/live/bot/ip.txt", "r") as infile:
        embed.set_footer(
            text=infile.read()
        )

    if lastTime is None:
        embed.add_field(
            name="Last Interaction",
            value="No recorded last interaction",
            inline=False
        )
    else:
        embed.add_field(
            name="Last Interaction",
            value=f"<t:{int(lastTime.timestamp())}:F>",
            inline=False
        )
        embed.add_field(
            name="Downtime",
            value=f"*{(datetime.now() - lastTime).total_seconds()}* seconds since last interaction."
        )

    embed.set_thumbnail(
        url=bot.user.display_avatar.url
    )

    chaos = await bot.fetch_user(SharkBot.IDs.dev)

    await chaos.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="nom nom nom!"))

    r = open("data/live/bot/reboot.txt", "r")
    replyTxt = r.read()
    replyFlag, replyID = replyTxt.split()
    r.close()

    if replyFlag == "True":
        replyChannel = await bot.fetch_channel(int(replyID))
        await replyChannel.send("I'm back!")
        w = open("data/live/bot/reboot.txt", "w")
        w.write(f"False {replyID}")
        w.close()

    print("\nThe bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"- {guild.name} : {guild.id}")
        print(f"    - Members: {len(guild.members)}")
        print(f"    - Text Channels: {len(guild.text_channels)}")
        print(f"    - Voice Channels: {len(guild.voice_channels)}")


@bot.command()
@commands.check_any(commands.is_owner())
async def reboot(ctx):
    await ctx.invoke(bot.get_command("pull"))
    await ctx.send("Alright! Rebooting now!")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))

    with open("data/live/bot/reboot.txt", "w+") as outfile:
        outfile.write("True " + str(ctx.channel.id))

    os.system("sudo reboot")


@bot.command()
@commands.is_owner()
async def restart(ctx) -> None:
    await ctx.invoke(bot.get_command("pull"))
    await ctx.send("Alright! Starting the script again!")

    with open("data/live/bot/reboot.txt", "w+") as outfile:
        outfile.write("True " + str(ctx.channel.id))
    with open("instant_restart", "w+") as outfile:
        pass

    quit()


@bot.command()
@commands.check_any(commands.is_owner())
async def load(message, extension):
    await bot.load_extension(f"cogs.{extension.lower()}")
    await message.channel.send(f"{extension.capitalize()} loaded.")


@bot.command()
@commands.check_any(commands.is_owner())
async def unload(message, extension):
    await bot.unload_extension(f"cogs.{extension.lower()}")
    await message.channel.send(f"{extension.capitalize()} unloaded.")


@bot.command()
@commands.check_any(commands.is_owner())
async def reload(ctx, extension="all"):
    extension = extension.lower()

    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                ext = filename[:-3]
                await bot.unload_extension(f"cogs.{ext}")
                await bot.load_extension(f"cogs.{ext}")
                await ctx.send(f"{ext.capitalize()} reloaded.")
                print(f"{ext.capitalize()} Cog reloaded.")
    else:
        await bot.unload_extension(f"cogs.{extension}")
        await bot.load_extension(f"cogs.{extension}")
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
    messageText = "Pulling latest commits..."
    message = await ctx.reply(f"```{messageText}```")
    messageText += "\n\n" + os.popen("git pull").read()
    await message.edit(content=f"```{messageText}```")


@bot.command()
@commands.is_owner()
async def reset(ctx):
    messageText = "git reset --hard"
    message = await ctx.reply(f"```{messageText}```")
    messageText += "\n\n" + os.popen("git reset --hard").read()
    await message.edit(content=f"```{messageText}```")


@bot.command()
@commands.is_owner()
async def execute(ctx, *, command):
    messageText = command
    message = await ctx.reply(f"```{messageText}```")
    messageText += "\n\n" + os.popen(command).read()
    await message.edit(content=f"```{messageText}```")


@bot.command()
@commands.check_any(commands.is_owner())
async def sync(ctx):
    message = await ctx.send("Syncing...")
    synced = await bot.tree.sync()
    message = await message.edit(content="Synced!")
    embed = discord.Embed()
    embed.title = "Command Sync"
    embed.description = f"{len(synced)} commands synced."
    commandList = ""
    for command in synced:
        commandList += f"**{command.name}** *[{','.join([argument.name for argument in command.options])}]*\n"
    embed.add_field(name="Slash Commands", value=commandList)
    await message.edit(embed=embed)


@bot.command()
@commands.check_any(commands.is_owner())
async def checkout(ctx, branch):
    os.system(f"git checkout {branch}")
    await ctx.send(f"Switched to {branch} branch.")
    os.system("git pull")
    await ctx.send("Pulling latest commits.")


async def main():

    raw_version = sys.version.split(" ")[0]
    version = [int(number) for number in raw_version.split(".")]
    if version[0] < 3 or version[1] < 10:
        print(f"Python 3.10 or newer must be used to run SharkBot. You are currently running {raw_version}")
        input("Press any key to exit...")
        quit()

    if not os.path.exists("data/live/bot/"):
        os.makedirs("data/live/bot")

    if not os.path.isfile("data/live/bot/reboot.txt"):
        with open("data/live/bot/reboot.txt", "w+") as rebootFile:
            rebootFile.write("False 0")

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ipify.org') as r:
            if r.status == 200:
                ip = await r.text()
                with open("data/live/bot/ip.txt", "w+") as outfile:
                    outfile.write(ip)
            else:
                if not os.path.exists("data/live/bot/ip.txt"):
                    with open("data/live/bot/ip.txt", "w+") as outfile:
                        outfile.write("0")


    print("\nBeginning SharkBot main()")

    print("\nLoaded Data:")
    print(f"- Loaded {len(SharkBot.Collection.collections)} Collections")
    print("\n".join([f"    - {c.name}: {c.length} items" for c in SharkBot.Collection.collections]))

    print(f"- Loaded data for {len(SharkBot.Member.members.values())} Members")

    print(f"\nLoading Cogs...\n")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print(f"\nFinished loading Cogs.")

    print("\nStarting Bot...")
    async with bot:
        await bot.start(secret.token)


asyncio.run(main())
