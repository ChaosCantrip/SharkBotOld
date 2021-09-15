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

    print("")
    print("The bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"{guild.name} : {guild.id}")



@bot.command()
async def tally(message):
    await count.tally(bot, message)



@bot.command()
async def reboot(message):
    if message.author.id != ids.users["Chaos"]:
        await message.channel.send("I'm afraid you're not allowed to do that!")
    else:
        await message.channel.send("Alright! Rebooting now!")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))

        os.system("sudo reboot")



@bot.command()
async def ping(message):
    await message.channel.send("Pong!")


@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return

        if message.author.id in ids.blacklist:
            return

        if message.channel.id == ids.channels["Count"] and count.check_is_count(message):

            if not await count.check_correct_number(message):
                await message.add_reaction("\N{EYES}")

            await count.update_list(bot, message)

        
            modRole = discord.utils.find(lambda r: r.id == ids.roles["Mod"], message.guild.roles)
            adminRole = discord.utils.find(lambda r: r.id == ids.roles["Admin"], message.guild.roles)

            if modRole in message.author.roles or adminRole in message.author.roles:
                if await count.check_admin_slowmode(message, 540):
                    await message.author.send("Naughty Naughty!")
                    await message.add_reaction("\N{NEUTRAL FACE}")

        await bot.process_commands(message)
    except Exception as e:
        await report_error(message, e)



bot.run(secret.token)
