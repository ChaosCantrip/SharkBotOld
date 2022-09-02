import discord
import random
import datetime
from discord.ext import tasks, commands
from definitions import Member, Item

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


def convert_to_num(message):
    result = ""

    for char in message.content:
        if char.isdigit():
            result = result + char

    if result == "":
        return None
    else:
        return int(result)


class Count(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def updatetally(self, ctx: commands.Context):
        channel = await self.bot.fetch_channel(ids.channels["Count"])

        outputText = "Working on it!"
        message = await ctx.send(f"```{outputText}```")
        outputText += "\n"

        for member in Member.members.values():
            member.set_counts(0)

        progress = 0
        async for pastMessage in channel.history(limit=None):
            progress += 1
            if progress % 200 == 0:
                outputText += f"\n{progress} messages processed..."
                await message.edit(content=f"```{outputText}```")

            if pastMessage.author.id in ids.blacklist:
                continue
            if convert_to_num(pastMessage) is None:
                continue

            member = Member.get(pastMessage.author.id)
            member.add_counts(1)

        outputText += "\n\nDone!"
        await message.edit(content=f"```{outputText}```")

        await self.tally(ctx)

    @commands.command()
    async def tally(self, ctx: commands.Context):
        server = await self.bot.fetch_guild(ids.server)
        memberNames = {member.id: member.display_name async for member in server.fetch_members()}

        members = [member for member in Member.members.values() if member.counts > 0]
        members.sort(key=lambda m: m.get_counts(), reverse=True)

        table = []
        lastCounts = 10000
        rank = 0
        trueRank = 0
        for member in members:
            trueRank += 1
            if member.get_counts() < lastCounts:
                lastCounts = member.get_counts()
                rank = trueRank

            memberName = memberNames[member.id] if member.id in memberNames else "*Exorcised Shark*"

            table.append({
                "name": memberName,
                "rank": rank,
                "counts": member.get_counts()
            })

        outputText = "\n".join([f"{row['rank']}. {row['name']} - {row['counts']}" for row in table])

        embed = discord.Embed()
        embed.title = "Count to 10,000"
        embed.description = outputText

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Count(bot))
    print("Count Cog loaded")


async def teardown(bot):
    print("Count Cog unloaded")
    await bot.remove_cog(Count(bot))
