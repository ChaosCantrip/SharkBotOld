import logging

import discord
from discord.ext import commands

import SharkBot

cog_logger = logging.getLogger("cog")

class Shop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def shop(self, ctx: commands.Context) -> None:
        embed = discord.Embed()
        embed.title = "Shop"
        embed.description = "Fucking Capitalists"
        for listing in SharkBot.Listing.listings:
            embed.add_field(
                name=f"{listing.item} - ${listing.price:,}",
                value=f"*{listing.item.description}*",
                inline=False
            )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def buy(self, ctx: commands.Context, search: str, quantity: str = "--") -> None:
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        search = search.lower()
        quantity = quantity.lower()

        try:
            item = SharkBot.Item.search(search)
        except SharkBot.Errors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return
        if item not in SharkBot.Listing.availableItems:
            await ctx.reply("I'm afraid you can't buy that!", mention_author=False)
            return

        listing = discord.utils.get(SharkBot.Listing.listings, item=item)

        if quantity == "--":
            num = 1
        elif quantity in ["max", "*"]:
            num = member.balance // listing.price
        else:
            try:
                num = int(quantity)
            except ValueError:
                await ctx.reply(f"`{quantity}` isn't a number I understand!")
                return

        if num <= 0:
            await ctx.reply(f"You can't buy `{num}` of something?!?")
            return

        if member.balance < num * listing.price:
            await ctx.reply(
                f"I'm afraid you don't have enough to buy **{str(item)}**",
                mention_author=False)
            return

        member.balance -= listing.price * num
        responses = member.inventory.add_items([item] * num)
        member.stats.boxes.bought += num

        embed = discord.Embed()
        embed.title = f"Bought {num}x {str(item)}"
        embed.description = f"You bought {num}x **{str(responses[0])}** for *${(listing.price * num):,}*"
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        await ctx.reply(embed=embed)

    @commands.hybrid_command()
    async def buy_cycle(self, ctx: commands.Context, *, search: str):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        box = SharkBot.Item.search(search)

        if box.type == "Item":
            await ctx.reply(f"**{str(box)}** isn't a lootbox!")
            return
        if not box.unlocked:
            await ctx.reply(f"**{str(box)}** is locked until <t:{int(box.unlock_dt.timestamp())}:d>!")
            return
        if box not in SharkBot.Listing.availableItems:
            await ctx.reply(f"**{str(box)}** isn't available in the shop!")
            return

        listing = discord.utils.get(SharkBot.Listing.listings, item=box)

        if member.balance < listing.price:
            await ctx.reply(f"I'm afraid you don't have enough to buy **{str(box)}** (${listing.price:,})")
            return

        embeds = []

        i = 0
        new_items = []
        boxes_cycled = 0
        while member.balance >= listing.price:
            i += 1

            boxes: list[SharkBot.Item.Lootbox] = [box] * (member.balance // listing.price)
            boxes_cycled += len(boxes)

            member.balance -= listing.price * len(boxes)
            member.inventory.add_items(boxes, ignore_vault=True)

            responses = [member.inventory.open_box(box) for box in boxes]
            items = [response.item for response in responses if not response.auto_vault]
            new_items.extend([response for response in responses if response.new_item])

            sold_sum = 0
            for item in items:
                sold_sum += item.value
                member.inventory.remove(item)

            member.balance += sold_sum

            if not member.settings.short_buy_cycle:
                embeds.append(discord.Embed())
                embeds[-1].title = f"Buy Cycling {str(box)} - Cycle {i}"
                embeds[-1].description = f"Bought {len(boxes)}x **{str(box)}**"

                embeds[-1].add_field(
                    name="Opened Items",
                    value="\n".join(str(response) for response in responses),
                    inline=False
                )

                embeds[-1].add_field(
                    name="Selling Items",
                    value=f"Sold {len(items)} items for *${sold_sum:,}*. Your new balance is *${member.balance:,}.*"
                )

        embeds.append(discord.Embed())
        embeds[-1].title = "Buy Cycle Finished"
        embeds[-1].description = f"You cycled through *{boxes_cycled:,}* boxes and discovered **{len(new_items):,}** new items!"

        if len(new_items) > 0:
            embeds[-1].add_field(
                name="__New Items__",
                value="\n".join(str(response) for response in new_items),
                inline=False
            )

        for embed in embeds:
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.display_avatar.url
            )
            embed.colour = box.collection.colour
            for e in SharkBot.Utils.split_embeds(embed):
                await ctx.reply(embed=e, mention_author=False)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.stats.boxes.bought += boxes_cycled
        member.stats.sold_items += boxes_cycled
        member.stats.boxes.opened += boxes_cycled

    @buy_cycle.autocomplete("search")
    async def buy_cycle_search_autocomplete(self, interaction: discord.Interaction, current: str):
        return await SharkBot.Autocomplete.shop_items(interaction, current)

async def setup(bot):
    await bot.add_cog(Shop(bot))
    print("Shop Cog Loaded")
    cog_logger.info("Shop Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Shop(bot))
    print("Shop Cog Unloaded")
    cog_logger.info("Shop Cog Unloaded")
