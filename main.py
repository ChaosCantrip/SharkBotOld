import asyncio
import os
from datetime import datetime, timedelta
import sys
import discord
from discord.ext import commands
import colorama
colorama.init(autoreset=True)

import secret
import SharkBot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"\nSharkBot connected to Discord" + colorama.Style.RESET_ALL)
    print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + f"- Account: {bot.user}")
    print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + f"- User ID: {bot.user.id}" + colorama.Style.RESET_ALL)

    await check_icons()

    if not os.path.exists("data/live/bot/lastmessage.txt"):
        last_time = None
    else:
        with open("data/live/bot/lastmessage.txt", "r") as infile:
            last_time = datetime.strptime(infile.read(), "%d/%m/%Y-%H:%M:%S:%f")

    embed = discord.Embed()
    embed.title = "SharkBot is up and running!"
    embed.description = f"<t:{int(datetime.now().timestamp())}:F>"

    if last_time is None:
        embed.add_field(
            name="Last Interaction",
            value="No recorded last interaction",
            inline=False
        )
    else:
        embed.add_field(
            name="Last Interaction",
            value=f"<t:{int(last_time.timestamp())}:F>",
            inline=False
        )
        embed.add_field(
            name="Downtime",
            value=f"*{(datetime.now() - last_time).total_seconds()}* seconds since last interaction."
        )

    embed.set_thumbnail(
        url=bot.user.display_avatar.url
    )

    chaos = await bot.fetch_user(SharkBot.IDs.dev)

    await chaos.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="nom nom nom!"))

    r = open("data/live/bot/reboot.txt", "r")
    reply_text = r.read()
    reply_flag, reply_id = reply_text.split()
    r.close()

    if reply_flag == "True":
        reply_channel = await bot.fetch_channel(int(reply_id))
        await reply_channel.send("I'm back!")
        w = open("data/live/bot/reboot.txt", "w")
        w.write(f"False {reply_id}")
        w.close()

    print("\nThe bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"- {guild.name} : {guild.id}")
        print(f"    - Members: {len(guild.members)}")
        print(f"    - Text Channels: {len(guild.text_channels)}")
        print(f"    - Voice Channels: {len(guild.voice_channels)}")


async def check_icons():
    guild = await bot.fetch_guild(SharkBot.IDs.icon_source_guild)
    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\nChecking Icons... ", end="")
    if not SharkBot.Icon.check(guild=guild):
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "New Icons Found.")
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + "Fetching new Icons... ", end="")
        SharkBot.Icon.extract(guild=guild)
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "Done.\n")
    else:
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "No New Icons Found.\n")

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
@commands.is_owner()
async def schedule_restart(ctx, secs: int) -> None:
    target_time = datetime.utcnow() + timedelta(seconds=secs)

    await ctx.send(f"Restart scheduled for {discord.utils.format_dt(target_time)}")
    await discord.utils.sleep_until(datetime.now() + timedelta(seconds=secs))

    await ctx.invoke(bot.get_command("pull"))
    await ctx.send(f"{ctx.author.mention} restarting...")

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
    message_text = "Pulling latest commits..."
    message = await ctx.reply(f"```{message_text}```")
    message_text += "\n\n" + os.popen("git pull").read()
    await message.edit(content=f"```{message_text}```")


@bot.command()
@commands.is_owner()
async def reset(ctx):
    message_text = "git reset --hard"
    message = await ctx.reply(f"```{message_text}```")
    message_text += "\n\n" + os.popen("git reset --hard").read()
    await message.edit(content=f"```{message_text}```")


@bot.command()
@commands.is_owner()
async def execute(ctx, *, command):
    message_text = command
    message = await ctx.reply(f"```{message_text}```")
    message_text += "\n\n" + os.popen(command).read()
    await message.edit(content=f"```{message_text}```")


@bot.command()
@commands.check_any(commands.is_owner())
async def sync(ctx):
    message = await ctx.send("Syncing...")
    synced = await bot.tree.sync()
    message = await message.edit(content="Synced!")
    embed = discord.Embed()
    embed.title = "Command Sync"
    embed.description = f"{len(synced)} commands synced."
    command_list = ""
    for command in synced:
        command_list += f"**{command.name}** *[{','.join([argument.name for argument in command.options])}]*\n"
    embed.add_field(name="Slash Commands", value=command_list)
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
    if version[0] < 3 or version[1] < 11:
        print(colorama.Fore.RED + colorama.Style.BRIGHT + "Python 3.11 or newer must be used to run SharkBot. You are currently running {raw_version}")
        input("Press any key to exit...")
        quit()

    SharkBot.Utils.FileChecker.file("data/live/bot/reboot.txt", "False 0")

    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\nBeginning SharkBot main()")

    print("\nLoaded Data:")
    print(f"- Loaded {len(SharkBot.Collection.collections)} Collections")
    print("\n".join([f"    - {c.name}: {len(c)} items" for c in SharkBot.Collection.collections]))

    print(f"- Loaded data for {len(SharkBot.Member.members)} Members")

    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\nLoading Cogs...\n")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"\nFinished loading Cogs.")

    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\nStarting Bot...")
    async with bot:
        await bot.start(secret.token)


asyncio.run(main())
