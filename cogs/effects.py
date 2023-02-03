import random
from datetime import timedelta, datetime

import discord
from discord.ext import tasks, commands

import SharkBot

import logging

cog_logger = logging.getLogger("cog")

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

    @commands.command()
    async def use(self, ctx: commands.Context, *, search: str):
        search = search.upper()
        search = " ".join(search.split())
        member = SharkBot.Member.get(ctx.author.id)
        if search.startswith("BINDER") or search.startswith("CON3"):
            await _UseHandler.use_binder(ctx, member, search)
            return
        if search.startswith("GOD'S BINDER") or search.startswith("GOD BINDER") or search.startswith("CON4"):
            await _UseHandler.use_god_binder(ctx, member, search)
            return
        split = search.split(" ")
        if split[-1] == "*":
            item = interpret_con_search(" ".join(split[:-1]), member)
            num = member.inventory.count(item)
        elif split[-1].isnumeric():
            num = int(split[-1])
            item = interpret_con_search(" ".join(split[:-1]), member, num)
        else:
            num = 1
            item = interpret_con_search(search, member, num)
        if num < 1:
            await ctx.reply(f"You can't use `{num}` of something!")
            return
        if item.type != "Consumable":
            await ctx.reply(f"**{member.view_of_item(item)}** is not a consumable item!")
            return
        has_count = member.inventory.count(item)
        if has_count == 0:
            await ctx.reply(f"I'm afraid you don't have any **{member.view_of_item(item)}**")
            return
        elif has_count < num:
            await ctx.reply(f"I'm afraid you only have **{has_count}x {member.view_of_item(item)}**")
            return

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name} used {num}x {item}"

        if item.name == "Loaded Dice":
            _UseHandler.use_loaded_dice(member, embed, num)
        elif item.name == "Counting Charm":
            _UseHandler.use_counting_charm(member, embed, num)
        elif item.name == "Lucky Clover":
            _UseHandler.use_lucky_clover(member, embed, num)
        elif item.name.startswith("Money Bag"):
            size = item.name.split(" ")[-1][1:-1]
            _UseHandler.use_money_bag(member, embed, size, num)
        elif item.name.startswith("Overclocker"):
            _UseHandler.use_overclocker(member, embed, num, item.name)
        elif item.name.startswith("XP Elixir"):
            size = item.name.split(" ")[-1][1:-1]
            _UseHandler.use_xp_elixir(member, embed, size, num)
        else:
            raise SharkBot.Errors.Effects.UnknownConsumableError(item.id, item.name)

        for i in range(num):
            member.inventory.remove(item)

        await ctx.reply(embed=embed, mention_author=False)


class _UseHandler:

    @staticmethod
    def use_loaded_dice(member: SharkBot.Member.Member, embed: discord.Embed, num: int):
        member.effects.add("Loaded Dice", charges=num)
        embed.description = f"You now have `{member.effects.get('Loaded Dice').charges}x` Active"

    @staticmethod
    async def use_binder(ctx: commands.Context, member: SharkBot.Member.Member, search: str):
        binder = SharkBot.Item.get("CON3")
        embed = discord.Embed()
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        if binder not in member.inventory:
            embed.title = f"{ctx.author.display_name} is trying to read air...?"
            embed.description = f"I'm afraid you don't have a **{member.view_of_item(binder)}** to use..."
            await ctx.reply(embed=embed, mention_author=False)
            return
        item_ids = search.split(" ")[1:]
        correct_usage = False
        if len(item_ids) == 0:
            embed.title = f"I don't think {ctx.author.display_name} knows how this works..."
            embed.description = "Please specify the **IDs** of the 3 items you would like to roll."
        elif item_ids[-1].isnumeric():
            embed.title = f"I think {ctx.author.display_name} is reading at a higher level"
            embed.description = f"I'm afraid you can only use one **{binder}** at once!"
        elif len(item_ids) < 3:
            embed.title = f"{ctx.author.display_name} is trying to cheat :("
            embed.description = "Please specify the IDs of the **THREE** items you would like to roll for."
        elif len(item_ids) > 3:
            embed.title = f"{ctx.author.display_name} is making things complicated..."
            embed.description = "Please just specify the IDs of *three* items you would like to roll for."
        elif len(item_ids) != len(set(item_ids)):
            embed.title = f"{ctx.author.display_name} is trying to cheat :("
            embed.description = "Please specify the IDs of the three **DIFFERENT** items you would like to roll for."
        else:
            correct_usage = True

        if not correct_usage:
            embed.description += "\n`$use binder ID1 ID2 ID3`"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed, mention_author=False)
            return

        items: list[SharkBot.Item.Item] = []
        errors = []
        for item_id in item_ids:
            try:
                items.append(SharkBot.Item.get(item_id))
            except SharkBot.Errors.ItemNotFoundError:
                errors.append(item_id)

        if len(errors) > 0:
            if len(errors) == 1:
                embed.description = f"I'm afraid `{errors[0]}` is not a valid item ID!"
            elif len(errors) == 2:
                embed.description = f"I'm afraid `{errors[0]}` and `{errors[1]}` are not valid item IDs!"
            else:
                embed.description = f"I'm afraid `{errors[0]}`, `{errors[1]}` and `{errors[2]}` are not valid item IDs!"
            embed.description += "\n`$use binder ID1 ID2 ID3`"
            embed.title = f"{ctx.author.display_name} is having a moment..."
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed, mention_author=False)
            return

        for item in items:
            if item.collection not in SharkBot.Collection.collections[0:5]:
                embed.title = f"{ctx.author.display_name} is looking for the impossible!"
                embed.description = f"I'm afraid **{item}** can't be found in this binder!"
                embed.colour = discord.Colour.red()
                await ctx.reply(embed=embed, mention_author=False)
                return

        embed.title = f"{ctx.author.display_name} is opening a Binder!"
        embed.description = f"What will they find? What will it be? Will they get 1, 2, or possibly 3?\n"
        embed.description += "\n".join(f"**{item}**" for item in items)
        embed.colour = discord.Colour.teal()
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/873771/screenshots/5839032/media/92e4c5665aee68c11eaac2025e7183b9.gif")
        message = await ctx.reply(embed=embed, mention_author=False)
        await discord.utils.sleep_until(datetime.utcnow() + timedelta(seconds=5))

        item = random.choice(items)
        member.inventory.remove(binder)
        response = member.inventory.add(item)

        embed.title = f"{ctx.author.display_name} opened a Binder!"
        embed.description = f"You got a **{response.item_printout}**!"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.colour = item.collection.colour
        await message.edit(embed=embed)

    @staticmethod
    async def use_god_binder(ctx: commands.Context, member: SharkBot.Member.Member, search: str):
        binder = SharkBot.Item.get("CON4")
        embed = discord.Embed()
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        if binder not in member.inventory:
            embed.title = f"{ctx.author.display_name} is trying to read air...?"
            embed.description = f"I'm afraid you don't have a **{member.view_of_item(binder)}** to use..."
            await ctx.reply(embed=embed, mention_author=False)
            return
        item_ids = search.split(" ")[2:]
        correct_usage = False
        if len(item_ids) == 0:
            embed.title = f"I don't think {ctx.author.display_name} knows how this works..."
            embed.description = "Please specify the **ID** of the item you would like to summon."
        elif item_ids[-1].isnumeric():
            embed.title = f"I think {ctx.author.display_name} is reading at a higher level"
            embed.description = f"I'm afraid you can only use one **{binder}** at once!"
        elif len(item_ids) > 1:
            embed.title = f"{ctx.author.display_name} is trying to cheat :("
            embed.description = "Please just specify the IDs of the **ONE** item you would like to summon."
        else:
            correct_usage = True

        if not correct_usage:
            embed.description += "\n`$use god's binder <ID>`"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed, mention_author=False)
            return

        try:
            item = SharkBot.Item.get(item_ids[0])
        except SharkBot.Errors.ItemNotFoundError:
            embed.title = f"{ctx.author.display_name} is having a moment..."
            embed.description = f"I'm afraid `{item_ids[0]}` is not a valid item ID!"
            embed.description += "\n`$use god's binder <ID>`"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed, mention_author=False)
            return

        if item.type != "Item" or item.collection == SharkBot.Collection.fragment:
            embed.title = f"{ctx.author.display_name} is looking for the impossible!"
            embed.description = f"I'm afraid **{item}** can't be found in this binder!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed, mention_author=False)
            return

        member.inventory.remove(binder)
        response = member.inventory.add(item)

        embed.title = f"{ctx.author.display_name} opened God's Binder!"
        embed.description = f"You got a **{response.item_printout}**!"
        embed.colour = item.collection.colour
        await ctx.reply(embed=embed, mention_author=False)

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
        super_effects = _overclocker_order[:index]
        if len(sub_effects) == 0:
            sub_effects = None
        if len(super_effects) == 0:
            super_effects = None

        hours = 4 * num
        member.effects.add(name, expiry=timedelta(hours=hours), sub_effects=sub_effects, super_effects=super_effects)
        until = member.effects.get(name).expiry - datetime.utcnow()
        embed.description = f"Each count for an additional `{hours} Hours` will reduce your cooldowns.\n"
        embed.description += "Any Overclocker of a lesser power will be paused until this one ends.\n"
        embed.description += f"**{name}** will be active for the next `{SharkBot.Utils.td_to_string(until)}`"

    @staticmethod
    def use_counting_charm(member: SharkBot.Member.Member, embed: discord.Embed, num: int):
        member.effects.add("Counting Charm", charges=num)
        embed.description = "When you count correctly, you will be guaranteed an item you have not collected, and spend one **Counting Charm** charge."
        embed.description += f"\nYou now have `{member.effects.get('Counting Charm').charges} Charges`"


def interpret_con_search(search: str, member: SharkBot.Member.Member, num: int = 1) -> SharkBot.Item.Item:
    try:
        return SharkBot.Item.search(search)
    except SharkBot.Errors.ItemNotFoundError:
        search = search.upper()
        if search in ["OVERCLOCKER", "MONEY BAG", "XP ELIXIR"]:
            for size in ["SMALL", "MEDIUM", "LARGE", "HUGE", "ULTIMATE"]:
                item = SharkBot.Item.search(f"{search} ({size})")
                print(f"{search} ({size})")
                if member.inventory.count(item) >= num:
                    return item
    raise SharkBot.Errors.ItemNotFoundError(search)



_overclocker_order = [
    "Overclocker (Ultimate)",
    "Overclocker (Huge)",
    "Overclocker (Large)",
    "Overclocker (Medium)",
    "Overclocker (Small)"
]

async def setup(bot):
    await bot.add_cog(Effects(bot))
    print("Effects Cog Loaded")
    cog_logger.info("Effects Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Effects(bot))
    print("Effects Cog Unloaded")
    cog_logger.info("Effects Cog Unloaded")