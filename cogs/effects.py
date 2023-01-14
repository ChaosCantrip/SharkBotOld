import random
from datetime import timedelta, datetime

import discord
from discord.ext import tasks, commands

import SharkBot

class Effects(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def effects(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Effects"
        embed.set_thumbnail(
            url=ctx.author.display_avatar.url
        )
        effects = member.effects.details
        if len(effects) > 0:
            embed.description = f"You have `{len(effects)}` effects active."
            for effect in effects:
                embed.add_field(
                    name=effect[0],
                    value=effect[1],
                    inline=False
                )
        else:
            embed.description = "You have no active effects."

        for e in SharkBot.Utils.split_embeds(embed):
            await ctx.reply(embed=e, mention_author=False)


class _UseHandler:

    @staticmethod
    def use_loaded_dice(member: SharkBot.Member.Member, num: int, embed: discord.Embed):
        member.effects.add("Loaded Dice", charges=num)
        embed.description = f"You now have `{member.effects.get('Loaded Dice').charges}x` Active"

    @staticmethod
    def use_binder(member: SharkBot.Member.Member, embed: discord.Embed):
        embed.description = "You used a Binder. Fuck you, I haven't implemented that yet."

    @staticmethod
    def use_god_binder(member: SharkBot.Member.Member, embed: discord.Embed):
        embed.description = "You used a God's Binder. Fuck you, I haven't implemented that yet."

    @staticmethod
    def use_money_bag(member: SharkBot.Member.Member, embed: discord.Embed, size: str, num: int):
        if size == "Small":
            low = 5
            high = 10
            hours = 1
        elif size == "Medium":
            low = 10
            high = 25
            hours = 2
        elif size == "Large":
            low = 25
            high = 50
            hours = 4
        elif size == "Huge":
            low = 50
            high = 100
            hours = 8
        elif size == "Ultimate":
            low = 100
            high = 250
            hours = 16
        else:
            raise SharkBot.Errors.Effects.InvalidSizeError("Money Bag", size)

        amount = sum(random.randint(low, high) for i in range(0, num))
        hours = hours * num
        member.balance += amount
        member.effects.add("Money Bag", expiry=timedelta(hours=hours))
        embed.description = f"You got **${amount}**, and will gain triple money from counting for a bonus `{hours} Hours`"

    @staticmethod
    def use_xp_elixir(member: SharkBot.Member.Member, embed: discord.Embed, size: str, num: int) -> int:
        if size == "Small":
            low = 1
            high = 3
            hours = 1
        elif size == "Medium":
            low = 3
            high = 5
            hours = 2
        elif size == "Large":
            low = 5
            high = 7
            hours = 4
        elif size == "Huge":
            low = 7
            high = 10
            hours = 8
        elif size == "Ultimate":
            low = 11
            high = 20
            hours = 16
        else:
            raise SharkBot.Errors.Effects.InvalidSizeError("XP Elixir", size)

        amount = sum(random.randint(low, high) for i in range(0, num))
        hours = hours * num
        member.effects.add("XP Elixir", expiry=timedelta(hours=hours))
        embed.description = f"You got `{amount} xp`, and will gain double XP from counting for a bonus `{hours} Hours`"
        return amount

    @staticmethod
    def use_lucky_clover(member: SharkBot.Member.Member, embed: discord.Embed, num: int):
        member.effects.add("Lucky Clover", charges=num)
        embed.description = "Whenever a correct count would not give you a Lootbox, you will instead be guaranteed one, and spend one **Lucky Clover** charge."
        embed.description += f"\nYou now have `{member.effects.get('Lucky Clover').charges} Charges`"

    @staticmethod
    def use_overclocker(member: SharkBot.Member.Member, embed: discord.Embed, num: int, name: str):
        index = _overclocker_order.index(name)
        sub_effects = _overclocker_order[index+1:]
        if len(sub_effects) == 0:
            sub_effects = None

        hours = 4 * num
        member.effects.add(name, expiry=timedelta(hours=hours), sub_effects=sub_effects)
        until = member.effects.get(name).expiry - datetime.utcnow()
        embed.description = "Each count for an additional `{hours} Hours` will reduce your cooldowns.\n"
        embed.description += "Any Overclocker of a lesser power will be paused until this one ends.\n"
        embed.description += f"**{name}** will be active for the next `{SharkBot.Utils.td_to_string(until)}`"


_overclocker_order = [
    "Overclocker (Ultimate)",
    "Overclocker (Huge)",
    "Overclocker (Large)",
    "Overclocker (Medium)",
    "Overclocker (Small)"
]

async def setup(bot):
    await bot.add_cog(Effects(bot))
    print("Effects Cog loaded")


async def teardown(bot):
    print("Effects Cog unloaded")
    await bot.remove_cog(Effects(bot))
