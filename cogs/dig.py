import subprocess
from datetime import datetime
from typing import Optional

import discord
from discord.ext import tasks, commands

import SharkBot

_DOMAINS_FILEPATH = "data/live/bot/dig.json"
SharkBot.Utils.FileChecker.json(_DOMAINS_FILEPATH, {})


class Dig(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.domains: dict[str, list[str]] = SharkBot.Utils.JSON.load(_DOMAINS_FILEPATH)
        self.target_channel: Optional[discord.TextChannel] = None

    def cog_unload(self) -> None:
        if self.dig_loop.is_running():
            self.dig_loop.stop()

    @tasks.loop(seconds=300)
    async def dig_loop(self):
        embed = discord.Embed(title="Dig", colour=discord.Colour.blue())
        embed.timestamp = datetime.utcnow()
        for domain, records in self.domains.items():
            for record in records:
                result = subprocess.run(f"dig {domain} +short {record}", shell=True, capture_output=True).stdout.decode()
                if result == "":
                    result = "No records found"
                embed.add_field(
                    name=f"{domain} ({record})",
                    value=f"```{result}```",
                    inline=False
                )
        await self.target_channel.send(embed=embed)

    @commands.group()
    async def dig(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @dig.command()
    async def add(self, ctx: commands.Context, domain: str, record: str):
        embed = discord.Embed(title="Dig Add", colour=discord.Colour.blue())
        domain = domain.lower()
        record = record.upper()
        if record in (record_list := self.domains.get(domain, [])):
            embed.description = f"`{record}` is already in dig list for `{domain}`"
        else:
            record_list.append(record)
            self.domains[domain] = record_list
            SharkBot.Utils.JSON.dump(_DOMAINS_FILEPATH, self.domains)
            embed.description = f"Added `{record}` to dig list for `{domain}`"
        await ctx.send(embed=embed)

    @dig.command()
    async def remove(self, ctx: commands.Context, domain: str, record: str):
        embed = discord.Embed(title="Dig Remove", colour=discord.Colour.blue())
        domain = domain.lower()
        record = record.upper()
        if domain == "*":
            self.domains = {}
            SharkBot.Utils.JSON.dump(_DOMAINS_FILEPATH, self.domains)
            embed.description = "Removed all dig records"
        elif record in (record_list := self.domains.get(domain, [])):
            record_list.remove(record)
            self.domains[domain] = record_list
            SharkBot.Utils.JSON.dump(_DOMAINS_FILEPATH, self.domains)
            embed.description = f"Removed `{record}` from dig list for `{domain}`"
        elif record == "*":
            self.domains.pop(domain)
            SharkBot.Utils.JSON.dump(_DOMAINS_FILEPATH, self.domains)
            embed.description = f"Removed all records from dig list for `{domain}`"
        else:
            embed.description = f"`{record}` is not in the dig list for `{domain}`"
        await ctx.send(embed=embed)

    @dig.command()
    async def list(self, ctx: commands.Context):
        embed = discord.Embed(title="Dig List", colour=discord.Colour.blue())
        for domain, records in self.domains.items():
            embed.add_field(
                name=f"```{domain}```",
                value=f"```{' | '.join(records)}```",
                inline=False
            )
        await ctx.send(embed=embed)

    @dig.command()
    async def start(self, ctx: commands.Context, interval: Optional[int] = None):
        if interval is not None:
            self.dig_loop.change_interval(seconds=interval)
        self.target_channel = ctx.channel
        self.dig_loop.start()
        embed = discord.Embed(title="Dig Start", colour=discord.Colour.blue())
        embed.description = f"Dig loop started with an interval of `{self.dig_loop.seconds}` seconds"
        await ctx.send(embed=embed)

    @dig.command()
    async def stop(self, ctx: commands.Context):
        self.dig_loop.cancel()
        embed = discord.Embed(title="Dig Stop", colour=discord.Colour.blue())
        embed.description = "Dig loop stopped"
        await ctx.send(embed=embed)

    @dig.command()
    async def status(self, ctx: commands.Context):
        embed = discord.Embed(title="Dig Status", colour=discord.Colour.blue())
        if self.dig_loop.is_running():
            embed.description = f"Dig loop is running with an interval of `{self.dig_loop.seconds}` seconds"
        else:
            embed.description = "Dig loop is not running"
        await ctx.send(embed=embed)

    @dig.command()
    async def interval(self, ctx: commands.Context, interval: int):
        self.dig_loop.change_interval(seconds=interval)
        embed = discord.Embed(title="Dig Interval", colour=discord.Colour.blue())
        embed.description = f"Dig loop interval changed to `{self.dig_loop.seconds}` seconds"
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dig(bot))
    print("Dig Cog loaded")


async def teardown(bot):
    print("Dig Cog unloaded")
    await bot.remove_cog(Dig(bot))
