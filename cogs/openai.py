from datetime import datetime, timedelta

import discord
from discord.ext import tasks, commands

import SharkBot


_usage_dict: dict[id, datetime] = {}


class OpenAI(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ask(self, ctx: commands.Context, *, prompt: str):
        if len(prompt) > 200:
            raise SharkBot.Errors.OpenAI.PromptTooLongError(prompt)
        if ctx.author.id in _usage_dict:
            if ctx.author.id == self.bot.owner_id:
                time_diff = None
            elif ctx.author.id in SharkBot.IDs.mods:
                time_diff = timedelta(minutes=5)
            else:
                time_diff = timedelta(hours=1)
            if time_diff is not None and datetime.now() - _usage_dict[ctx.author.id] < time_diff:
                raise SharkBot.Errors.OpenAI.TooManyRequestsError(time_diff)
        embed = discord.Embed()
        embed.title = prompt
        embed.description = "Thinking..."
        embed.set_author(
            name=ctx.author.display_name + " asked...",
            icon_url=ctx.author.display_avatar.url
        )
        embed.set_thumbnail(
            url="https://miro.medium.com/v2/resize:fit:400/1*mMTHT8fwuCvSSp0RNXM4nA.gif"
        )
        message = await ctx.reply(embed=embed, mention_author=False)
        response = await SharkBot.Handlers.openaiHandler.ask_sharkbot(prompt)
        embed.description = response[1]["choices"][0]["message"]["content"]
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await message.edit(embed=embed)
        _usage_dict[ctx.author.id] = datetime.now()


async def setup(bot):
    await bot.add_cog(OpenAI(bot))
    print("OpenAI Cog loaded")


async def teardown(bot):
    print("OpenAI Cog unloaded")
    await bot.remove_cog(OpenAI(bot))
