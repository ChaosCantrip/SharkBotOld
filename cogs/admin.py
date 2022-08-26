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


async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("Admin Cog loaded")


async def teardown(bot):
    print("Admin Cog unloaded")
    await bot.remove_cog(Admin(bot))
