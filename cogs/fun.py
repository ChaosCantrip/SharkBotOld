from datetime import datetime, timedelta, time

import discord
from discord.ext import tasks, commands

import random

from humanize import number

import SharkBot


import logging

cog_logger = logging.getLogger("cog")

class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_birthdays.start()

    def cog_unload(self) -> None:
        self.check_birthdays.cancel()

    @commands.hybrid_command(
        aliases=["cf"],
        brief="Bet an amount of SharkCoins on a coin flip to get double or nothing back!"
    )
    async def coinflip(self, ctx, amount: int) -> None:
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        embed = discord.Embed()
        embed.title = "Coin Flip"
        embed.description = f"You bet **${amount:,}**!"
        embed.set_thumbnail(url="https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")

        if amount < 0:
            embed.colour = discord.Color.red()
            embed.add_field(
                name="Negative Bet!",
                value="You can't bet a negative amount of money!"
            )
            await ctx.reply(embed=embed)
            return

        if amount == 0:
            embed.colour = discord.Color.red()
            embed.add_field(
                name="Zero Bet!",
                value="You can't bet zero SharkCoins!!"
            )
            await ctx.reply(embed=embed)
            return

        if member.balance < amount:
            embed.colour = discord.Color.red()
            embed.add_field(
                name="Not Enough Money!",
                value=f"You don't have **${amount:,}**!"
            )
            await ctx.reply(embed=embed)
            return

        roll = random.randint(1, 16)
        if roll <= 7:  # Win
            member.balance += amount
            member.stats.coinflips.wins += 1
            embed.colour = discord.Color.green()
            embed.add_field(
                name="You win!",
                value=f"You won **${amount:,}**!"
            )
        elif roll <= 9:  # Mercy Loss
            embed.colour = discord.Color.blurple()
            member.stats.coinflips.mercies += 1
            embed.add_field(
                name="You lose!",
                value=f"You lost, but I'm feeling nice, so I'll let you keep your money!"
            )
        else:  # Loss
            member.balance -= amount
            member.stats.coinflips.losses += 1
            embed.colour = discord.Color.dark_red()
            embed.add_field(
                name="You lose!",
                value=f"You lost **${amount:,}**!"
            )
        await ctx.reply(embed=embed)
        await member.missions.log_action("coinflip", ctx, amount)

    @coinflip.autocomplete("amount")
    async def coinflip_amount_autocomplete(self, interaction: discord.Interaction, current: str):
        return await SharkBot.Autocomplete.member_balance(interaction, current)

    @commands.hybrid_group()
    async def birthday(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        date = datetime.now().date()

        embed = discord.Embed()
        embed.title = "Birthday"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        if member.birthday is None:
            embed.description = "Your birthday is not set! Set it with *$birthday set `dd` `mm` `yyyy`*."
        elif date == member.birthday:
            embed.description = "Your birthday is today! Happy Birthday!!!"
        else:
            embed.description = f"Your birthday is set to `{datetime.strftime(member.birthday, SharkBot.Member.BIRTHDAY_FORMAT)}`"

        await ctx.send(embed=embed)

    @birthday.command()
    async def set(self, ctx: commands.Context, day: int, month: int, year: int):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        embed = discord.Embed()
        embed.title = "Set Birthday"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        if len(str(year)) != 4:
            embed.description = "Please use the format `dd` `mm` `yyyy`"
            await ctx.send(embed=embed)
            return

        try:
            member.birthday = datetime(year, month, day).date()
            embed.description = f"Set your Birthday to `{datetime.strftime(member.birthday, SharkBot.Member.BIRTHDAY_FORMAT)}`."
            await ctx.send(embed=embed)
        except ValueError:
            embed.description = "Please enter a valid date."
            await ctx.send(embed=embed)

    @tasks.loop(time=time(hour=12))
    async def check_birthdays(self):
        today = datetime.today()
        presents = [
            SharkBot.Item.get("LOOTSHARK"),
            SharkBot.Item.get("LOOTSHARK"),
            SharkBot.Item.get("LOOTSHARK"),
            SharkBot.Item.get("LOOTM"),
            SharkBot.Item.get("E10")
        ]
        channel = await self.bot.fetch_channel(SharkBot.IDs.channels["SharkBot Commands"])

        for member in SharkBot.Member.members:
            if member.birthday is None:
                continue
            if member.birthday.day == today.day and member.birthday.month == today.month:
                if member.lastClaimedBirthday < today.year:
                    member.lastClaimedBirthday = today.year
                    responses = member.inventory.add_items(presents)
                    member.write_data()
                    age = number.ordinal(today.year - member.birthday.year)
                    user = await channel.guild.fetch_member(member.id)

                    embed = discord.Embed()
                    embed.title = "Birthday Time!"
                    embed.description = f"It's **{user.display_name}**'s {age} Birthday! I got them:\n"
                    embed.description += "\n".join(str(response) for response in responses)
                    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

                    await channel.send(f"{user.mention}", embed=embed)

    @commands.hybrid_command()
    async def remind_me(self, ctx: commands.Context, minutes: int, message: str):
        await ctx.reply("Noted.", mention_author=False)
        await discord.utils.sleep_until(datetime.now() + timedelta(minutes=minutes))
        await ctx.send(f"{ctx.author.mention}\n\"{message}\"")

    @commands.hybrid_group()
    async def count_message(self, ctx: commands.Context):
        await ctx.invoke(self.bot.get_command("count_message list"))

    @count_message.command()
    async def add(self, ctx: commands.Context, *, message: str):
        if "[ITEM]" not in message:
            await ctx.reply("I'm afraid contributions need to contain the phrase [ITEM] (with the square brackets) for me to know where to put the item name")
            return
        if len(message) > 500:
            await ctx.reply("I'm afraid Counting Box Messages need to be shorter than 500 characters!")
            return
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        messages = SharkBot.CountBoxMessage.get_member(ctx.author.id)
        if messages is None:
            num = 0
        else:
            num = len(messages)
        if num >= member.xp.level:
            await ctx.reply("I'm afraid you've used up all your message slots! Increase your SharkBot level to add more, or use `/count_message remove` to remove one to replace!")
            return
        try:
            SharkBot.CountBoxMessage.add(ctx.author.id, message)
        except SharkBot.Errors.CountBoxMessageExistsError:
            await ctx.reply("I'm afraid a similar message already exists in the pool. Great minds think alike, eh?")
            return

        item = SharkBot.Item.FakeItem(random.choice(SharkBot.Item.items))
        item.name = "Test Item"
        used_text = f"**{item}**".join(message.split("[ITEM]"))
        await ctx.reply(f"Added '{used_text}' to the counting box message pool - Thank You!")

    @add.autocomplete("message")
    async def add_message_autocomplete(self, interaction: discord.Interaction, current: str):
        if len(current) > 500:
            return [
                discord.app_commands.Choice(
                    name="Message must be <500 characters!",
                    value=current[0:499]
                )
            ]
        else:
            return [
                discord.app_commands.Choice(
                    name=f"{current} [ITEM]",
                    value=f"{current} [ITEM]"
                )
            ]

    @count_message.command()
    async def remove(self, ctx: commands.Context, message_id: int):
        message = SharkBot.CountBoxMessage.get(ctx.author.id, message_id)
        messages = SharkBot.CountBoxMessage.get_member(ctx.author.id)
        if messages is None:
            await ctx.reply("You don't have any counting messages contributed!\nUse `/count_message add` to add your first!")
            return
        if message is None:
            await ctx.reply("I couldn't find a message with that ID sorry, use `/count_message remove` to see them better.")
            return
        SharkBot.CountBoxMessage.remove(ctx.author.id, message_id)
        item = SharkBot.Item.FakeItem(random.choice(SharkBot.Item.items))
        item.name = "Test Item"
        used_text = f"**{item}**".join(message.split("[ITEM]"))
        await ctx.reply(f"Removed '{used_text}' from the counting box message pool.")

    @remove.autocomplete("message_id")
    async def remove_message_id_autocomplete(self, interaction: discord.Interaction, current: str):
        current = current.lower()
        member = SharkBot.Member.get(interaction.user.id)
        messages = SharkBot.CountBoxMessage.get_member(interaction.user.id)
        if messages is None:
            return [
                discord.app_commands.Choice(
                    name="You don't have any to remove...",
                    value=-1
                )
            ]
        else:
            return [
                discord.app_commands.Choice(
                    name=f"{num} - {text}",
                    value=num
                ) for num, text in messages.items() if text.lower().startswith(current)
            ]

    @count_message.command()
    async def list(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        messages = SharkBot.CountBoxMessage.get_member(ctx.author.id)
        embed = discord.Embed()
        embed.title = "Counting Box Messages"
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        if messages is None:
            embed.description = "You don't have any counting messages contributed.\nUse `/count_message add` to add your first!"
        else:
            embed.description = f"You have {len(messages)} counting messages contributed."
            embed.add_field(
                name="__Your Contributions__",
                value="\n".join(f"`{num}` - {message}" for num, message in messages.items()),
                inline=False
            )
        embed.set_footer(text=f"You can contribute a number of messages up to your SharkBot level - `{member.xp.level}`")
        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot):
    await bot.add_cog(Fun(bot))
    print("Fun Cog Loaded")
    cog_logger.info("Fun Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Fun(bot))
    print("Fun Cog Unloaded")
    cog_logger.info("Fun Cog Unloaded")