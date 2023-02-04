from typing import Literal

import discord
from discord import app_commands
from discord.ext import tasks, commands

import SharkBot

class Settings(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="settings", usage="$settings <setting> <enabled>")
    async def settings(self, ctx: commands.Context, setting: Literal["delete_incorrect_counts"], enabled: bool):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        if setting == "delete_incorrect_counts":
            member.settings.delete_incorrect_counts = enabled
        await ctx.reply(f"Set `{setting}` to `{enabled}`")

    @settings.command()
    async def list(self, ctx: commands.Context):
        await ctx.reply("Settings List")



async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("Settings Cog loaded")


async def teardown(bot):
    print("Settings Cog unloaded")
    await bot.remove_cog(Settings(bot))
