import discord
from discord.ext import tasks, commands
from handlers import databaseHandler
from definitions import SharkErrors

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def migrate(self, ctx, *, newChannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        currentChannel = ctx.author.voice.channel
        members = list(currentChannel.members)
        for member in members:
            await member.move_to(newChannel)
        await ctx.send(f"Moved *{len(members)}* members from {currentChannel.mention} to {newChannel.mention}.")

    @commands.command()
    async def boop(self, ctx, member: discord.Member):
        await member.edit(mute=False)
        await ctx.send(f"Unmuted {member.display_name}")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def summon(self, ctx, *, targetChannel: discord.VoiceChannel):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
            return
        currentChannel = ctx.author.voice.channel
        members = list(targetChannel.members)
        for member in members:
            await member.move_to(currentChannel)
        await ctx.send(f"Moved *{len(members)}* members from {targetChannel.mention} to {currentChannel.mention}.")

    @commands.command()
    @commands.is_owner()
    async def upload_all(self, ctx):
        databaseHandler.upload_all_members()
        await ctx.send("```Done!```")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def testerror(self, ctx):
        raise SharkErrors.TestError()



def setup(bot):
    bot.add_cog(Admin(bot))
    print("Admin Cog loaded")


def teardown(bot):
    print("Admin Cog unloaded")
    bot.remove_cog(Admin(bot))
