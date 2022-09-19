import asyncio

import discord
from discord.ext import tasks, commands
from SharkBot import IDs


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_role(IDs.roles["Mod"])
    async def migrate(self, ctx, *, newchannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        currentChannel = ctx.author.voice.channel
        members = list(currentChannel.members)
        for member in members:
            await member.move_to(newchannel)
        await ctx.send(f"Moved *{len(members)}* members from {currentChannel.mention} to {newchannel.mention}.")

    @commands.hybrid_command()
    @commands.has_role(IDs.roles["Mod"])
    async def summon(self, ctx, *, targetchannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        members = list(targetchannel.members)
        currentChannel = ctx.author.voice.channel
        for member in members:
            await member.move_to(currentChannel)
        await ctx.send(f"Moved *{len(members)}* members from {targetchannel.mention} to {currentChannel.mention}.")

    @commands.hybrid_command()
    @commands.has_role(IDs.roles["Mod"])
    async def grab(self, ctx, target: discord.Member):
        targetChannel = ctx.author.voice.channel

        message = await ctx.reply(f"Waiting to grab {target.display_name}.")

        if target.voice is not None:
            await target.move_to(targetChannel)
            await message.reply(f"Moved {target.display_name} to {targetChannel.mention}")
            return

        def check(m, b, a):
            return m.id == target.id and a.channel is not None

        try:
            member, before, after = await self.bot.wait_for("voice_state_update", check=check, timeout=600)
        except asyncio.TimeoutError:
            await message.reply("Grab timed out!")
        else:
            await member.move_to(targetChannel)
            await message.reply(f"Moved {target.display_name} to {targetChannel.mention}")


async def setup(bot):
    await bot.add_cog(Voice(bot))
    print("Voice Cog loaded")


async def teardown(bot):
    print("Voice Cog unloaded")
    await bot.remove_cog(Voice(bot))
