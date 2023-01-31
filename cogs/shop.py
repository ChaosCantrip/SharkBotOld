import discord
from discord.ext import commands

from SharkBot import Listing, Member, Errors, Item, Views, Utils


class Shop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def shop(self, ctx: commands.Context) -> None:
        embed = discord.Embed()
        embed.title = "Shop"
        embed.description = "Fucking Capitalists"
        for listing in Listing.listings:
            embed.add_field(
                name=f"{listing.item} - ${listing.price:,}",
                value=f"*{listing.item.description}*",
                inline=False
            )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def buy(self, ctx: commands.Context, search: str, quantity: str = "--") -> None:
        member = Member.get(ctx.author.id)
        search = search.lower()
        quantity = quantity.lower()

        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return
        if item not in Listing.availableItems:
            await ctx.reply("I'm afraid you can't buy that!", mention_author=False)
            return

        listing = discord.utils.get(Listing.listings, item=item)

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
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        await ctx.reply(embed=embed)
        member.write_data()

    @commands.command()
    async def buy_cycle(self, ctx: commands.Context, *, search: str):
        member = Member.get(ctx.author.id)
        box = Item.search(search)

        if box.type == "Item":
            await ctx.reply(f"**{str(box)}** isn't a lootbox!")
            return
        if not box.unlocked:
            await ctx.reply(f"**{str(box)}** is locked until <t:{int(box.unlock_dt.timestamp())}:d>!")
            return
        if box not in Listing.availableItems:
            await ctx.reply(f"**{str(box)}** isn't available in the shop!")
            return

        listing = discord.utils.get(Listing.listings, item=box)

        if member.balance < listing.price:
            await ctx.reply(f"I'm afraid you don't have enough to buy **{str(box)}** (${listing.price:,})")
            return

        embeds = []

        i = 0
        new_items = 0
        boxes_cycled = 0
        while member.balance >= listing.price:
            i += 1
            embeds.append(discord.Embed())
            embeds[-1].set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url
            )
            embeds[-1].title = f"Buy Cycling {str(box)} - Cycle {i}"

            boxes: list[Item.Lootbox] = [box] * (member.balance // listing.price)
            member.balance -= listing.price * len(boxes)
            member.inventory.add_items(boxes, ignore_vault=True)
            embeds[-1].description = f"Bought {len(boxes)}x **{str(box)}**"

            items = []
            responses = []
            for box in boxes:
                boxes_cycled += 1
                item = box.roll()
                member.inventory.remove(box)
                response = member.inventory.add(item)
                if not response.auto_vault:
                    items.append(item)
                responses.append(response)

            field_lines = []
            for response in responses:
                if response.new_item:
                    new_items += 1
                field_lines.append(str(response))

            embeds[-1].add_field(
                name="Opened Items",
                value="\n".join(field_lines),
                inline=False
            )

            sold_sum = 0
            for item in items:
                sold_sum += item.value
                member.inventory.remove(item)

            member.balance += sold_sum

            embeds[-1].add_field(
                name="Selling Items",
                value=f"Sold {len(items)} items for *${sold_sum:,}*. Your new balance is *${member.balance:,}.*"
            )

        embeds.append(discord.Embed())
        embeds[-1].set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )
        embeds[-1].title = "Buy Cycle Finished"
        embeds[-1].description = f"You cycled through *{boxes_cycled:,}* boxes and discovered **{new_items:,}** new items!"

        for embed in embeds:
            for e in Utils.split_embeds(embed):
                await ctx.reply(embed=e, mention_author=False)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.stats.boxes.bought += boxes_cycled
        member.stats.sold_items += boxes_cycled
        member.stats.boxes.opened += boxes_cycled
        member.write_data()


async def setup(bot):
    await bot.add_cog(Shop(bot))
    print("Shop Cog loaded")


async def teardown(bot):
    print("Shop Cog unloaded")
    await bot.remove_cog(Shop(bot))
