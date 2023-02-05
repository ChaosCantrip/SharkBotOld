from typing import Literal

import discord
from discord import app_commands
from discord.ext import tasks, commands

import SharkBot

class Settings(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="settings", usage="$settings <setting> <enabled>")
    async def settings(self, ctx: commands.Context, setting: Literal["delete_incorrect_counts"], enabled: bool):
        # TODO: Add Embed to command
        # TODO: Implement as callable slash command
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        if setting == "delete_incorrect_counts":
            member.settings.delete_incorrect_counts = enabled
        await ctx.reply(f"Set `{setting}` to `{enabled}`", mention_author=False)

    @commands.hybrid_command(name="settings_list")
    async def settings_list(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        embed = discord.Embed(
            title="Settings",
            colour=discord.Colour.blurple()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.description = f" - `delete_incorrect_counts` -> `{member.settings.delete_incorrect_counts}`"
        await ctx.reply(embed=embed, mention_author=False)



async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("Settings Cog loaded")


async def teardown(bot):
    print("Settings Cog unloaded")
    await bot.remove_cog(Settings(bot))
