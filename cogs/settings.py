from typing import Literal

import discord
from discord import app_commands
from discord.ext import tasks, commands

import SharkBot

class Settings(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="settings")
    async def settings(self, interaction: discord.Interaction, setting: Literal["delete_incorrect_counts"], enabled: bool):
        # TODO: Add Embed to command
        # TODO: Implement as callable slash command
        member = SharkBot.Member.get(interaction.user.id, discord_user=interaction.user)
        if setting == "delete_incorrect_counts":
            member.settings.delete_incorrect_counts = enabled
        await interaction.response.send_message(f"Set `{setting}` to `{enabled}`")

    @app_commands.command(name="settings_list")
    async def settings_list(self, interaction: discord.Interaction):
        # TODO: Implement Command
        await interaction.response.send_message("Settings List")



async def setup(bot):
    await bot.add_cog(Settings(bot))
    print("Settings Cog loaded")


async def teardown(bot):
    print("Settings Cog unloaded")
    await bot.remove_cog(Settings(bot))
