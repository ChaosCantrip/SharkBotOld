import os

import discord
import psutil
from discord.ext import commands

import secret
from SharkBot import SharkErrors, Member

if secret.testBot:
    import testids as ids
else:
    import ids


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def upload_all(self, ctx: commands.Context) -> None:
        outputText = "Uploading all Member Data!\n"
        message = await ctx.send(f"```{outputText}```")
        for member in Member.members.values():
            member.upload_data()
            outputText += f"\nUploaded {member.id}'s data"
            await message.edit(content=f"```{outputText}```")
        outputText += "\n\nDone!"
        await message.edit(content=f"```{outputText}```")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def test_error(self, ctx: commands.Context) -> None:
        raise SharkErrors.TestError()

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def clean_members(self, ctx: commands.Context) -> None:
        userIDs = [user.id for user in self.bot.users]
        messageOutput = "Cleaning members...\n"
        message = await ctx.send(f"```{messageOutput}```")
        kept = 0
        removed = 0
        for member in list(Member.members.values()):
            if member.id not in userIDs:
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
    async def get_emojis(self, ctx: commands.Context) -> None:
        for emoji in ctx.guild.emojis:
            await ctx.send(f"<:{emoji.name}:{emoji.id}:>")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def system_status(self, ctx: commands.Context) -> None:
        vm = psutil.virtual_memory()

        totalMB = "{:,.2f} MB".format(vm.total/(1024*1024))
        totalGB = "{:,.2f} GB".format(vm.total/(1024*1024*1024))
        usedMB = "{:,.2f} MB".format(vm.used/(1024*1024))
        usedGB = "{:,.2f} GB".format(vm.used/(1024*1024*1024))
        freeMB = "{:,.2f} MB".format(vm.free/(1024*1024))
        freeGB = "{:,.2f} GB".format(vm.free/(1024*1024*1024))
        percent = f"{vm.percent}%"

        process = psutil.Process(os.getpid()).memory_info()
        processMB = "{:,.2f} MB".format(process.rss / 1024 ** 2)
        processGB = "{:,.2f} GB".format(process.rss / 1024 ** 3)
        processPercentUsed = "{:,.2f}% Used".format((process.rss / vm.used) * 100)
        processPercentTotal = "{:,.2f}% Total".format((process.rss / vm.total) * 100)

        embed = discord.Embed()
        embed.colour = discord.Color.greyple()
        embed.title = "System Status"
        embed.add_field(
            name="Total RAM",
            value=f"{totalMB}\n{totalGB}"
        )
        embed.add_field(
            name="Used RAM",
            value=f"{usedMB}\n{usedGB}"
        )
        embed.add_field(
            name="Free RAM",
            value=f"{freeMB}\n{freeGB}"
        )
        embed.add_field(
            name="Percentage Free RAM",
            value=f"{percent}"
        )
        embed.add_field(
            name="Used by Python",
            value=f"{processMB}\n{processGB}\n{processPercentUsed}\n{processPercentTotal}"
        )

        await ctx.send(embed=embed)

    @commands.hybrid_group()
    @commands.has_role(ids.roles["Mod"])
    async def purge(self, ctx: commands.Context) -> None:
        await ctx.send("Purge Command")

    @purge.command()
    @commands.has_role(ids.roles["Mod"])
    async def last(self, ctx: commands.Context, number: int) -> None:
        message = await ctx.reply(f"```Deleting last {number} messages.```")
        deleted = await ctx.channel.purge(limit=number, before=discord.Object(ctx.message.id))
        await message.edit(content=f"```Deleted last {len(deleted)} messages.```")

    @purge.command()
    @commands.has_role(ids.roles["Mod"])
    async def to(self, ctx: commands.Context, target: discord.Message) -> None:
        message = await ctx.reply(f"```Deleting up to {target.id}.```")
        deleted = await ctx.channel.purge(before=discord.Object(ctx.message.id), after=discord.Object(target.id))
        await message.edit(content=f"```Deleted {len(deleted)} messages.")

    @purge.command()
    @commands.has_role(ids.roles["Mod"])
    async def member(self, ctx: commands.Context, target: discord.Member, limit: int = 100) -> None:
        message = await ctx.reply(f"```Deleting messages from {target.display_name} in last {limit} messages.```")
        deleted = await ctx.channel.purge(
            limit=limit,
            check=lambda m: m.author.id == target.id,
            before=discord.Object(ctx.message.id)
        )
        await message.edit(content=f"```Deleted {len(deleted)} messages from {target.display_name}.```")


async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("Admin Cog loaded")


async def teardown(bot):
    print("Admin Cog unloaded")
    await bot.remove_cog(Admin(bot))
