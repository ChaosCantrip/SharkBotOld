import json

import discord
from discord.ext import tasks, commands
from definitions import SharkErrors, Member

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_role(ids.roles["Mod"])
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
    @commands.has_role(ids.roles["Mod"])
    async def summon(self, ctx, *, targetchannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        members = list(targetchannel.members)
        currentChannel = ctx.author.voice.channel
        for member in members:
            await member.move_to(currentChannel)
        await ctx.send(f"Moved *{len(members)}* members from {targetchannel.mention} to {currentChannel.mention}.")

    @commands.command()
    @commands.is_owner()
    async def upload_all(self, ctx):
        outputText = "Uploading all memberdata!\n"
        message = await ctx.send(f"```{outputText}```")
        for member in Member.members.values():
            member.upload_data()
            outputText += f"\nUploaded {member.id}'s data"
            await message.edit(content=f"```{outputText}```")
        outputText += "\n\nDone!"
        await message.edit(content=f"```{outputText}```")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def testerror(self, ctx):
        raise SharkErrors.TestError()

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def cleanmembers(self, ctx):
        userids = [user.id for user in self.bot.users]
        messageOutput = "Cleaning members...\n"
        message = await ctx.send(f"```{messageOutput}```")
        kept = 0
        removed = 0
        for member in list(Member.members.values()):
            if member.id not in userids:
                messageOutput += f"\nRemoved {member.id}."
                await message.edit(content=f"```{messageOutput}```")
                member.delete_file()
                removed += 1
            else:
                kept += 1
        messageOutput += f"\n\nRemoved {removed} members, kept {kept}."
        await message.edit(content=f"```{messageOutput}```")
        Member.load_member_files()


async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("Admin Cog loaded")


async def teardown(bot):
    print("Admin Cog unloaded")
    await bot.remove_cog(Admin(bot))
