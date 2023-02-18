from typing import Literal

import discord
from discord.ext import commands

import SharkBot


class Settings(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="settings", usage="$settings <setting> <enabled>")
    async def settings(self, ctx: commands.Context, setting: Literal["delete_incorrect_counts", "short_buy_cycle"], enabled: bool):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        if setting == "delete_incorrect_counts":
            member.settings.delete_incorrect_counts = enabled
        elif setting == "short_buy_cycle":
            member.settings.short_buy_cycle = enabled
        else:
            await ctx.reply("I... How did you even get past the `Literal` check? You're drunk, go home.")
            return
        embed = discord.Embed(
            title="Settings",
            colour=discord.Colour.blurple()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f"Set `{setting}` to `{enabled}`"
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="settings_list")
    async def settings_list(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        embed = discord.Embed(
            title="Settings",
            colour=discord.Colour.blurple()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f" - `delete_incorrect_counts` -> `{member.settings.delete_incorrect_counts}`"
        embed.description += f"\n - `short_buy_cycle` -> `{member.settings.short_buy_cycle}`"
        await ctx.reply(embed=embed, mention_author=False)



async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("Settings Cog loaded")


async def teardown(bot):
    print("Settings Cog unloaded")
    await bot.remove_cog(Settings(bot))
