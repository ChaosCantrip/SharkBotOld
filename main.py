import asyncio
import os

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

if secret.testBot:
    import testids as ids
else:
    import ids


@bot.event
async def on_ready():
    print("\nSharkBot connected to Discord")
    print(f"- Account: {bot.user}")
    print(f"- User ID: {bot.user.id}")

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

    f = open("reboot.txt", "w")
    f.write("True " + str(ctx.channel.id))
    f.close()

    os.system("sudo reboot")


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

print(f"\nLoaded {len(SharkBot.Collection.collections)} Collections")
print("\n".join([f"    - {c.name}: {c.length} items" for c in SharkBot.Collection.collections]))


async def main():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

    async with bot:
        await bot.start(secret.token)


asyncio.run(main())
