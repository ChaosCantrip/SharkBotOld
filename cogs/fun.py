from datetime import datetime

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

    @commands.hybrid_command(
        aliases=["cf"],
        brief="Bet an amount of SharkCoins on a coin flip to get double or nothing back!"
    )
    async def coinflip(self, ctx, amount: int) -> None:
        member = Member.get(ctx.author.id)
        embed = discord.Embed()
        embed.title = "Coin Flip"
        embed.description = f"You bet **${amount}**!"
        embed.set_thumbnail(url="https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")

        if amount < 0:
            embed.colour = discord.Color.red()
            embed.add_field(
                name="Negative Bet!",
                value="You can't bet a negative amount of money!"
            )
            await ctx.reply(embed=embed)
            return

        if member.get_balance() < amount:
            embed.colour = discord.Color.red()
            embed.add_field(
                name="Not Enough Money!",
                value=f"You don't have **${amount}**!"
            )
            await ctx.reply(embed=embed)
            return

        roll = random.randint(1, 16)
        if roll <= 7:  # Win
            member.add_balance(amount)
            embed.colour = discord.Color.green()
            embed.add_field(
                name="You win!",
                value=f"You won **${amount}**!"
            )
        elif roll <= 9:  # Mercy Loss
            embed.colour = discord.Color.blurple()
            embed.add_field(
                name="You lose!",
                value=f"You lost, but I'm feeling nice, so I'll let you keep your money!"
            )
        else:  # Loss
            member.add_balance(-amount)
            embed.colour = discord.Color.dark_red()
            embed.add_field(
                name="You lose!",
                value=f"You lost **${amount}**!"
            )
        await ctx.reply(embed=embed)
        await member.missions.log_action("coinflip", ctx.author)
        member.write_data()

    @commands.hybrid_group()
    async def birthday(self, ctx: commands.Context):
        member = Member.get(ctx.author.id)
        date = datetime.now().date()

        embed = discord.Embed()
        embed.title = "Birthday"
        embed.set_author(name=ctx.author.display_name, url=ctx.author.avatar.url)

        if member.birthday is None:
            embed.description = "Your birthday is not set! Set it with *$birthday set <dd> <mm> <yyyy>."
        elif date == member.birthday:
            embed.description = "Your birthday is today! Happy Birthday!!!"
        else:
            embed.description = f"Your birthday is set to `{datetime.strftime(member.birthday, Member.birthdayFormat)}`"

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Fun(bot))
    print("Fun Cog loaded")


async def teardown(bot):
    print("Fun Cog unloaded")
    await bot.remove_cog(Fun(bot))
