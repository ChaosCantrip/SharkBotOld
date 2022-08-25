import discord
from discord.ext import tasks, commands

import secret
import random
from definitions import Member

if secret.testBot:
    import testids as ids
else:
    import ids


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command()
    async def coinflip(self, ctx, amount: int) -> None:
        member = Member.get(ctx.author.id)

        if member.get_balance() < amount:
            await ctx.reply(f"You don't have ${amount} to bet!")
            return

        member.add_balance(-amount)
        roll = random.randint(1,2)
        if roll == 1:   ## Win
            member.add_balance(2*amount)
            await ctx.reply(f"You win! You bet ${amount} and won ${2*amount}!")
        else: # Loss
            mercyroll = random.randint(1,8)
            if mercyroll == 1:
                member.add_balance(amount)
                await ctx.reply(f"You lose! You lost ${amount}, but I'm feeling nice, so I'll let you have it back!")
            else:
                await ctx.reply(f"You lose! You bet ${amount} and lost!")


async def setup(bot):
    await bot.add_cog(Fun(bot))
    print("Fun Cog loaded")


async def teardown(bot):
    print("Fun Cog unloaded")
    await bot.remove_cog(Fun(bot))
