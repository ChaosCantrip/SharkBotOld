import logging
from datetime import datetime

import discord
from discord.ext import commands

import SharkBot

cog_logger = logging.getLogger("cog")
app_command_logger = logging.getLogger("app_command")

class Core(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        member.write_data()

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command: discord.app_commands.Command | discord.app_commands.ContextMenu):
        member = SharkBot.Member.get(interaction.user.id, discord_user=interaction.user)
        app_command_logger.info(f"{member.id} {member.raw_display_name} - /{command.name}")
        member.write_data()


    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("Pong!")

    @commands.command()
    async def pingtime(self, ctx: commands.Context) -> None:
        text = f"Pong!\nMessage Received={(datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000}ms"
        message = await ctx.send(text)
        text += f"\nPing={(message.created_at - ctx.message.created_at).total_seconds() * 1000}ms"
        await message.edit(content=text)

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx: commands.Context, channel: discord.TextChannel, *, text: str) -> None:
        await ctx.reply(f"Sending \"{text}\" to {channel.mention}.", mention_author=False)
        await channel.send(text)


async def setup(bot):
    await bot.add_cog(Core(bot))
    print("Core Cog Loaded")
    cog_logger.info("Core Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Core(bot))
    print("Core Cog Unloaded")
    cog_logger.info("Core Cog Unloaded")