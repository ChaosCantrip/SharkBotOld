import discord
from discord.ext import tasks, commands
from asyncio import TimeoutError
from SharkBot import Member

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setbalance", aliases=["setbal"], brief="Sets the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def set_balance(self, ctx, target: discord.Member, amount: int):
        member = Member.get(target.id)
        member.balance = amount
        await ctx.send(f"Set {target.display_name}'s balance to {amount}.")
        member.write_data()

    @commands.command(name="addbalance", aliases=["addbal", "addfunds"],
                      brief="Adds to the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def add_balance(self, ctx, target: discord.Member, amount: int):
        member = Member.get(target.id)
        member.balance += amount
        await ctx.send(f"{amount} added to {target.display_name}'s account.")
        member.write_data()

    @commands.command(name="getbalance", aliases=["getbal"], brief="Returns the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def get_balance(self, ctx, target: discord.Member):
        member = Member.get(target.id)
        bal = member.balance

        embed = discord.Embed()
        embed.title = "Balance Check"
        embed.description = f"**{target.display_name}**'s balance is: *${bal}*"
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.colour = 0x00836d
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["bal", "econ"], brief="Returns the user's SharkCoin balance.")
    async def balance(self, ctx):
        await ctx.invoke(self.bot.get_command("getbalance"), target=ctx.author)

    @commands.command(aliases=["transfer"])
    async def pay(self, ctx, target: discord.Member, amount: int):
        member = Member.get(ctx.author.id)
        targetMember = Member.get(target.id)
        if amount < 0:
            await ctx.send("Nice try buddy. Please enter a positive amount!")
            return

        if member.balance < amount:
            await ctx.send("Sorry, you don't have enough coins to do that.")
            return

        message = await ctx.send(f"Transfer {amount} to {target.display_name}?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda react, author: author == ctx.author and react.message == message and react.emoji in ["✅", "❌"]

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except TimeoutError:
            await message.edit(content="Transfer cancelled, timed out.")
            return

        if reaction.emoji == "✅":
            member.balance -= amount
            targetMember.balance += amount
            await message.edit(content=f"Transferred {amount} to {target.display_name}.")
        else:
            await message.edit(content="Transfer cancelled.")
        member.write_data()

        targetMember.write_data()


async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("Economy Cog loaded")


async def teardown(bot):
    print("Economy Cog unloaded")
    await bot.remove_cog(Economy(bot))
