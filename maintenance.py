import asyncio
import os
import traceback

import discord
from discord.ext import commands
import colorama
colorama.init(autoreset=True)

import secret

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"\nMaintenance Bot connected to Discord")
    print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + f"- Account: {bot.user}")
    print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + f"- User ID: {bot.user.id}")

    chaos = await bot.fetch_user(220204098572517376)

    await chaos.send("SharkBot has entered maintenance mode")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Maintenance Mode."))


@bot.command()
@commands.is_owner()
async def end(ctx: commands.Context) -> None:
    await ctx.send("Ok! Restoring functionality!")

    if os.path.exists("maintenance"):
        os.remove("maintenance")

    quit()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("SharkBot is currently in Maintenance Mode! Please stand by until normal functionality is restored.", mention_author=False)
        return
    elif isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingPermissions):
        await ctx.reply("I'm afraid you don't have permission to do that!", mention_author=False)
        return
    else:
        dev = await bot.fetch_user(220204098572517376)
        embed = discord.Embed()
        embed.title = "Error Report"
        embed.description = "Maintenance Mode Error"
        error_type = type(error)
        print(f"{error_type.__module__}.{error_type.__name__}{error.args}")
        error_name = f"{error_type.__module__}.{error_type.__name__}{error.args}"
        embed.add_field(name="Type", value=error_name, inline=False)
        embed.add_field(name="Args", value=error.args, inline=False)
        embed.add_field(name="Traceback", value="\n".join(traceback.format_tb(error.__traceback__)))
        await dev.send(embed=embed)


async def main():

    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\nStarting Maintenance Bot...")
    async with bot:
        await bot.start(secret.token)


asyncio.run(main())
