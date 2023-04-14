import os
from typing import Optional

import discord
from discord.ext import tasks, commands

import SharkBot

_DOMAINS_FILEPATH = "data/live/bot/dig.json"
SharkBot.Utils.FileChecker.json(_DOMAINS_FILEPATH, [])
_RECORDS = ["NS", "A", "AAAA"]


class Dig(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.domains: list[str] = SharkBot.Utils.JSON.load(_DOMAINS_FILEPATH)

    def cog_unload(self) -> None:
        if self.dig_loop.is_running():
            self.dig_loop.stop()

    @tasks.loop(seconds=300)
    async def dig_loop(self):
        embed = discord.Embed(title="Dig", colour=discord.Colour.blue())
        for domain in self.domains:
            for record in _RECORDS:
                result = os.system(f"dig {domain} +noall +answer -t {record}")
                embed.add_field(
                    name=f"{domain} ({record})",
                    value=f"```{result}```",
                    inline=False
                )
        dev = await self.bot.fetch_user(SharkBot.IDs.dev)
        await dev.send(embed=embed)

    @commands.group()
    async def dig(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @dig.command()
    async def add(self, ctx: commands.Context, domain: str):
        domain = domain.lower()
        if domain not in self.domains:
            self.domains.append(domain)
            SharkBot.Utils.JSON.dump(_DOMAINS_FILEPATH, self.domains)
            await ctx.send(f"Added {domain} to dig list")
        else:
            await ctx.send(f"{domain} is already in the dig list")

    @dig.command()
    async def remove(self, ctx: commands.Context, domain: str):
        domain = domain.lower()
        if domain in self.domains:
            self.domains.remove(domain)
            SharkBot.Utils.JSON.dump(_DOMAINS_FILEPATH, self.domains)
            await ctx.send(f"Removed {domain} from dig list")
        else:
            await ctx.send(f"{domain} is not in the dig list")

    @dig.command()
    async def list(self, ctx: commands.Context):
        await ctx.send(f"```{SharkBot.Utils.JSON.dumps(self.domains)}```")

    @dig.command()
    async def start(self, ctx: commands.Context, interval: Optional[int] = None):
        if interval is not None:
            self.dig_loop.change_interval(seconds=interval)
        self.dig_loop.start()
        await ctx.send("Dig loop started")

    @dig.command()
    async def stop(self, ctx: commands.Context):
        self.dig_loop.stop()
        await ctx.send("Dig loop stopped")

    @dig.command()
    async def status(self, ctx: commands.Context):
        await ctx.send(f"Dig loop is running: {self.dig_loop.is_running()}")

    @dig.command()
    async def interval(self, ctx: commands.Context, interval: int):
        self.dig_loop.change_interval(seconds=interval)
        await ctx.send(f"Dig loop interval changed to {interval} seconds")


async def setup(bot):
    await bot.add_cog(Dig(bot))
    print("Dig Cog loaded")


async def teardown(bot):
    print("Dig Cog unloaded")
    await bot.remove_cog(Dig(bot))
