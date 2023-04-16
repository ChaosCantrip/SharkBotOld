import json
from datetime import datetime, timedelta

import discord
from discord.ext import tasks, commands

import SharkBot


class OpenAI(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._usage_dict = {}

    @commands.command()
    async def ask(self, ctx: commands.Context, *, prompt: str):
        await self.ask_sharkbot_wrapper(ctx.message, prompt)

    @commands.command()
    async def draw(self, ctx: commands.Context, *, prompt: str):
        await self.draw_sharkbot_wrapper(ctx.message, prompt)

    async def ask_sharkbot_wrapper(self, message: discord.Message, prompt: str):
        if len(prompt) > 200:
            raise SharkBot.Errors.OpenAI.PromptTooLongError(prompt)
        embed = discord.Embed()
        embed.title = prompt
        embed.description = "Thinking..."
        embed.set_author(
            name=message.author.display_name + " asked...",
            icon_url=message.author.display_avatar.url
        )
        embed.set_thumbnail(
            url="https://miro.medium.com/v2/resize:fit:400/1*mMTHT8fwuCvSSp0RNXM4nA.gif"
        )
        message = await message.reply(embed=embed, mention_author=False)
        response = await SharkBot.Handlers.openaiHandler.ask_sharkbot(prompt)
        embed.description = response[1]["choices"][0]["message"]["content"]
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await message.edit(embed=embed)
        self._usage_dict[message.author.id] = datetime.now()

    async def draw_sharkbot_wrapper(self, message: discord.Message, prompt: str):
        if len(prompt) > 200:
            raise SharkBot.Errors.OpenAI.PromptTooLongError(prompt)
        if message.author.id in self._usage_dict:
            if message.author.id == SharkBot.IDs.dev:
                time_diff = None
            elif message.author.id in SharkBot.IDs.mods:
                time_diff = timedelta(minutes=1)
            else:
                time_diff = timedelta(minutes=10)
            if time_diff is not None and datetime.now() - self._usage_dict[message.author.id] < time_diff:
                raise SharkBot.Errors.OpenAI.TooManyRequestsError(time_diff)
        embed = discord.Embed()
        embed.title = prompt
        embed.description = "Drawing..."
        embed.set_author(
            name=message.author.display_name + " asked for...",
            icon_url=message.author.display_avatar.url
        )
        embed.set_thumbnail(
            url="https://miro.medium.com/v2/resize:fit:400/1*mMTHT8fwuCvSSp0RNXM4nA.gif"
        )
        reply_message = await message.reply(embed=embed, mention_author=False)
        try:
            status, response = await SharkBot.Handlers.openaiHandler.make_image_request(prompt)
        except SharkBot.Errors.OpenAI.BadPromptError as e:
            embed.description = "Oh my cod! I couldn't draw that!"
            embed.colour = discord.Colour.red()
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            await message.edit(embed=embed)
            return
        embed.description = "Done!"
        embed.set_image(url=response["data"][0]["url"])
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await reply_message.edit(embed=embed)
        self._usage_dict[message.author.id] = datetime.now()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if not message.content.startswith(self.bot.user.mention):
            return
        prompt = " ".join(message.clean_content.split(" ")[1:])
        try:
            if prompt.lower().startswith("draw"):
                await self.draw_sharkbot_wrapper(message, prompt[5:])
            else:
                await self.ask_sharkbot_wrapper(message, prompt)
        except Exception as e:
            if isinstance(e, SharkBot.Errors.SharkError):
                await e.handler(message)
            else:
                raise e



async def setup(bot):
    await bot.add_cog(OpenAI(bot))
    print("OpenAI Cog loaded")


async def teardown(bot):
    print("OpenAI Cog unloaded")
    await bot.remove_cog(OpenAI(bot))
