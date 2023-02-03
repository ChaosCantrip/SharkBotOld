from datetime import datetime
import logging

import discord
from discord.ext import commands

import SharkBot

import logging

cog_logger = logging.getLogger("cog")

class Core(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)
        member.discord_user = ctx.author
        member.write_data()

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("Pong!")

    @commands.command()
    async def pingtime(self, ctx: commands.Context) -> None:
        text = f"Pong!\nMessage Received={(datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000}ms"
        message = await ctx.send(text)
        text += f"\nPing={(message.created_at - ctx.message.created_at).total_seconds() * 1000}ms"
        await message.edit(content=text)

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx: commands.Context, channel: discord.TextChannel, *, text: str) -> None:
        await ctx.reply(f"Sending \"{text}\" to {channel.mention}.", mention_author=False)
        await channel.send(text)

    @commands.hybrid_command()
    async def myid(self, ctx: commands.Context) -> None:
        await ctx.send(f"Your ID is: *{ctx.author.id}*")

    @commands.hybrid_command()
    async def simp(self, ctx: commands.Context) -> None:
        embed = discord.Embed()
        embed.title = "Click here to access your SIMP Profile"
        embed.description = "SharkBot Inventory Manager Prototype"
        embed.set_author(name=ctx.author.display_name)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = f"https://test.chaoscantrip.com/redirect.php?memberid={ctx.author.id}"
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Core(bot))
    print("Core Cog Loaded")
    cog_logger.info("Core Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Core(bot))
    print("Core Cog Unloaded")
    cog_logger.info("Core Cog Unloaded")