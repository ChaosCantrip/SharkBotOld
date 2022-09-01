import json
import os

import discord, psutil
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
        
    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def getemojis(self, ctx):
        for emoji in ctx.guild.emojis:
            await ctx.send(f"<:{emoji.name}:{emoji.id}:>")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def systemstatus(self, ctx):
        vm = psutil.virtual_memory()

        totalmb = "{:,.2f} MB".format(vm.total/(1024*1024))
        totalgb = "{:,.2f} GB".format(vm.total/(1024*1024*1024))
        usedmb = "{:,.2f} MB".format(vm.used/(1024*1024))
        usedgb = "{:,.2f} GB".format(vm.used/(1024*1024*1024))
        freemb = "{:,.2f} MB".format(vm.free/(1024*1024))
        freegb = "{:,.2f} GB".format(vm.free/(1024*1024*1024))
        percent = f"{vm.percent}%"

        process = psutil.Process(os.getpid()).memory_info()
        processmb = "{:,.2f} MB".format(process.rss / 1024 ** 2)
        processgb = "{:,.2f} GB".format(process.rss / 1024 ** 3)
        processpercent = "{:,.2f}%".format((process.rss / vm.total) * 100)

        embed = discord.Embed()
        embed.color = discord.Color.greyple()
        embed.title = "System Status"
        embed.add_field(
            name="Total RAM",
            value=f"{totalmb}\n{totalgb}"
        )
        embed.add_field(
            name="Used RAM",
            value=f"{usedmb}\n{usedgb}"
        )
        embed.add_field(
            name="Free RAM",
            value=f"{freemb}\n{freegb}"
        )
        embed.add_field(
            name="Percentage Free RAM",
            value=f"{percent}"
        )
        embed.add_field(
            name="Used by Python",
            value=f"{processmb}\n{processgb}\n{processpercent}"
        )

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("Admin Cog loaded")


async def teardown(bot):
    print("Admin Cog unloaded")
    await bot.remove_cog(Admin(bot))
