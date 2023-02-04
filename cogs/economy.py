from typing import Union, Literal

import discord
from discord.ext import commands

from SharkBot import Member, IDs


import logging

cog_logger = logging.getLogger("cog")

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setbalance", aliases=["setbal"], brief="Sets the target's SharkCoin balance.")
    @commands.has_role(IDs.roles["Mod"])
    async def set_balance(self, ctx, target: discord.Member, amount: int):
        member = Member.get(target.id)
        member.balance = amount
        await ctx.send(f"Set {target.display_name}'s balance to ${amount:,}.")
        member.write_data()

    @commands.command(name="addbalance", aliases=["addbal", "addfunds"],
                      brief="Adds to the target's SharkCoin balance.")
    @commands.has_role(IDs.roles["Mod"])
    async def add_balance(self, ctx, target: discord.Member, amount: int):
        member = Member.get(target.id)
        member.balance += amount
        await ctx.send(f"${amount:,} added to {target.display_name}'s account.")
        member.write_data()

    @commands.command(name="getbalance", aliases=["getbal"], brief="Returns the target's SharkCoin balance.")
    @commands.has_role(IDs.roles["Mod"])
    async def get_balance(self, ctx, target: discord.Member):
        member = Member.get(target.id)

        embed = discord.Embed()
        embed.title = f"{target.display_name}'s Balance"
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.description = f"Wallet Balance: **${member.balance:,}**"
        embed.description += f"\nBank Balance: **${member.bank_balance:,}**"
        embed.colour = 0x00836d
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["bal", "econ"], brief="Returns the user's SharkCoin balance.")
    async def balance(self, ctx):
        await ctx.invoke(self.bot.get_command("getbalance"), target=ctx.author)

    @commands.command(aliases=["transfer"])
    async def pay(self, ctx, target: discord.Member, amount: int):
        member = Member.get(ctx.author.id, discord_user=ctx.author)
        target_member = Member.get(target.id)

        if amount < 0:
            await ctx.send("Nice try buddy. Please enter a positive amount!")
            return
        if member.balance < amount:
            await ctx.send("Sorry, you don't have enough SharkCoins to do that.")
            return

        member.balance -= amount
        target_member.balance += amount
        await ctx.reply(f"Sent **${amount:,}** to {target.mention}.", mention_author=False)

        target_member.write_data()

    @commands.group(invoke_without_command=True)
    async def bank(self, ctx: commands.Context):
        member = Member.get(ctx.author.id, discord_user=ctx.author)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Bank Balance"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f"You have **${member.bank_balance:,}** in your bank."

        await ctx.reply(embed=embed, mention_author=False)

    @bank.command()
    async def deposit(self, ctx: commands.Context, amount: Union[int, float, str] = "*"):
        member = Member.get(ctx.author.id, discord_user=ctx.author)
        if type(amount) == float:
            amount = int(amount)
        if type(amount) == str:
            if amount.lower() in ["all", "*"]:
                amount = member.balance
            else:
                await ctx.reply(f"Sorry, '{amount}' isn't a valid amount!")
                return
        if amount <= 0:
            await ctx.reply(f"The amount to deposit must be above **$0**!")
            return

        if amount > member.balance:
            await ctx.reply(f"You don't have **${amount:,}** to deposit! Your balance is only **${member.balance:,}**.")
            return

        member.balance -= amount
        member.bank_balance += amount

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Bank Deposit"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f"You deposited **${amount}** into your bank!"
        embed.description += f"\nNew Wallet Balance: **${member.balance}**"
        embed.description += f"\nNew Bank Balance: **${member.bank_balance}**"

        await ctx.reply(embed=embed, mention_author=False)

    @bank.command()
    async def withdraw(self, ctx: commands.Context, amount: Union[int, float, str] = "*"):
        member = Member.get(ctx.author.id, discord_user=ctx.author)
        if type(amount) == float:
            amount = int(amount)
        if type(amount) == str:
            if amount.lower() in ["all", "*"]:
                amount = member.bank_balance
            else:
                await ctx.reply(f"Sorry, '{amount}' isn't a valid amount!")
                return
        if amount <= 0:
            await ctx.reply(f"The amount to withdraw must be above **$0**!")
            return

        if amount > member.bank_balance:
            await ctx.reply(
                f"You don't have **${amount:,}** to withdraw! Your bank balance is only **${member.bank_balance:,}**."
            )
            return

        member.bank_balance -= amount
        member.balance += amount

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Bank Withdrawal"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f"You withdrew **${amount:,}** from your bank!"
        embed.description += f"\nNew Wallet Balance: **${member.balance:,}**"
        embed.description += f"\nNew Bank Balance: **${member.bank_balance:,}**"

        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("Economy Cog Loaded")
    cog_logger.info("Economy Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Economy(bot))
    print("Economy Cog Unloaded")
    cog_logger.info("Economy Cog Unloaded")