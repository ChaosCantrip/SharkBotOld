import json

import discord
from discord.ext import tasks, commands
from handlers import databaseHandler
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
        databaseHandler.upload_all_members()
        await ctx.send("```Done!```")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def testerror(self, ctx):
        raise SharkErrors.TestError()

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def migratemembers(self, ctx):
        with open("data/memberdata.json", "r") as infile:
            data = json.load(infile)
        for memberid, memberdata in data.items():
            with open(f"data/members/{memberid}.json", "w") as outfile:
                json.dump(memberdata, outfile)
                await ctx.send(f"```Migrated {memberid}'s data```")
        Member.load_member_files()
        await ctx.send("Done!")


async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("Admin Cog loaded")


async def teardown(bot):
    print("Admin Cog unloaded")
    await bot.remove_cog(Admin(bot))
