import discord
from discord.ext import tasks, commands
from datetime import datetime

import SharkBot


class Christmas(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def advent(self, ctx: commands.Context):
        dt_now = datetime.now()

        embed = discord.Embed()
        embed.title = "Advent Calendar"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        if dt_now.month < 12:
            embed.description = "Advent Calendar starts on **December 1st**!"
        else:
            if dt_now.day > 25:
                embed.description = "Advent Calendar ended on **December 25th**! Merry Christmas!"
            else:
                member = SharkBot.Member.get(ctx.author.id)
                if True: # Day > Member.last_advent_claimed
                    gift = SharkBot.Advent.get_day(dt_now.day-1)
                    member.inventory.add(gift)
                    embed.description = f"You got: **{str(gift)}**!"
                else:
                    embed.description = "You've already claimed your advent calendar today!"

        await ctx.reply(embed=embed, mention_author=False)




async def setup(bot):
    await bot.add_cog(Christmas(bot))
    print("Christmas Cog loaded")


async def teardown(bot):
    print("Christmas Cog unloaded")
    await bot.remove_cog(Christmas(bot))
