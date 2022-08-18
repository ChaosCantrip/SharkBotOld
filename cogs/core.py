import datetime

import discord
from discord.ext import commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Core(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def pingtime(self, ctx):
        await ctx.send(f"Pong! t={(datetime.datetime.now() - ctx.message.created_at).total_seconds() * 1000}ms")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def getdata(self, ctx):
        await ctx.send("Working!", file=discord.File("data/memberdata.json"))

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, text):
        await channel.send(text)

    @commands.command()
    async def myid(self, ctx):
        await ctx.send(f"Your ID is: *{ctx.author.id}*")

    @commands.command()
    async def simp(self, ctx):
        await ctx.send(f"https://test.chaoscantrip.com/?memberid={ctx.author.id}")


async def setup(bot):
    await bot.add_cog(Core(bot))
    print("Core Cog loaded")


async def teardown(bot):
    print("Core Cog unloaded")
    await bot.remove_cog(Core(bot))
