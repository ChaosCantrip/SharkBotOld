import discord
from discord.ext import tasks, commands

import SharkBot


class OpenAI(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def ask(self, ctx: commands.Context, *, prompt: str):
        message = await ctx.reply("Working on it...", mention_author=False)
        response = await SharkBot.Handlers.openaiHandler.ask_sharkbot(prompt)
        await message.edit(content=response[1]["choices"][0]["message"]["content"])



async def setup(bot):
    await bot.add_cog(OpenAI(bot))
    print("OpenAI Cog loaded")


async def teardown(bot):
    print("OpenAI Cog unloaded")
    await bot.remove_cog(OpenAI(bot))
