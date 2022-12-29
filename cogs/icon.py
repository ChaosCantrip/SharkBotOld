import discord
from discord.ext import commands

import SharkBot


class Icon(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def icon_list(self, ctx):
        embed = discord.Embed()
        embed.title = "Icon List"
        for name, icon in SharkBot.Icon.icon_dict().items():
            embed.add_field(
                name=f"{icon} {name}",
                value=f"`{icon}`",
                inline=False
            )

        for e in SharkBot.Utils.split_embeds(embed):
            await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(Icon(bot))
    print("Icon Cog loaded")


async def teardown(bot):
    print("Icon Cog unloaded")
    await bot.remove_cog(Icon(bot))
