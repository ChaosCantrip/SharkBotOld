import asyncio

import discord
from discord.ext import commands

import SharkBot


import logging

cog_logger = logging.getLogger("cog")

class Voice(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    @SharkBot.Checks.is_mod()
    async def migrate(self, ctx, *, newchannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        current_channel = ctx.author.voice.channel
        members = list(current_channel.members)
        for member in members:
            await member.move_to(newchannel)
        await ctx.send(f"Moved *{len(members)}* members from {current_channel.mention} to {newchannel.mention}.")

    @commands.hybrid_command()
    @SharkBot.Checks.is_mod()
    async def summon(self, ctx, *, targetchannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        members = list(targetchannel.members)
        current_channel = ctx.author.voice.channel
        for member in members:
            await member.move_to(current_channel)
        await ctx.send(f"Moved *{len(members)}* members from {targetchannel.mention} to {current_channel.mention}.")

    @commands.hybrid_command()
    @SharkBot.Checks.is_mod()
    async def grab(self, ctx, target: discord.Member):
        target_channel = ctx.author.voice.channel

        message = await ctx.reply(f"Waiting to grab {target.display_name}.")

        if target.voice is not None:
            await target.move_to(target_channel)
            await message.reply(f"Moved {target.display_name} to {target_channel.mention}")
            return

        # noinspection PyUnusedLocal
        def check(m, b, a):
            return m.id == target.id and a.channel is not None

        try:
            member, before, after = await self.bot.wait_for("voice_state_update", check=check, timeout=600)
        except asyncio.TimeoutError:
            await message.reply("Grab timed out!")
        else:
            await member.move_to(target_channel)
            await message.reply(f"Moved {target.display_name} to {target_channel.mention}")

    @commands.command()
    @SharkBot.Checks.is_mod()
    async def retreat(self, ctx: commands.Context):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        current_channel = ctx.author.voice.channel
        mod_channel = await self.bot.fetch_channel(SharkBot.IDs.channels["Mod Channel"])
        members = list(current_channel.members)
        for member in members:
            if member.id in SharkBot.IDs.mods:
                await member.move_to(mod_channel)



async def setup(bot):
    await bot.add_cog(Voice(bot))
    print("Voice Cog Loaded")
    cog_logger.info("Voice Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Voice(bot))
    print("Voice Cog Unloaded")
    cog_logger.info("Voice Cog Unloaded")