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
                name=f"{listing.item} - ${listing.price}",
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
        for i in range(num):
            member.balance -= listing.price
            member.inventory.add(item)
            member.stats.boughtBoxes += 1

        embed = discord.Embed()
        embed.title = f"Bought {num}x {str(item)}"
        embed.description = f"You bought {num}x {str(item)} for *${listing.price * num}*"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        view = Views.BuyView([item] * num, ctx.author.id, embed)

        view.message = await ctx.reply(embed=embed, view=view)
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
            await ctx.reply(f"I'm afraid you don't have enough to buy **{str(box)}** (${listing.price})")
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
            member.inventory.add_items(boxes)
            embeds[-1].description = f"Bought {len(boxes)}x **{str(box)}**"

            items = []
            for box in boxes:
                boxes_cycled += 1
                item = box.roll()
                items.append((item, not member.collection.contains(item)))
                member.inventory.remove(box)
                member.inventory.add(item)

            field_lines = []
            for item, new in items:
                if new:
                    new_items += 1
                    field_lines.append(f"{str(item)} :sparkles:")
                else:
                    field_lines.append(f"{str(item)}")

            embeds[-1].add_field(
                name="Opened Items",
                value="\n".join(field_lines),
                inline=False
            )

            sold_sum = 0
            for item in [tup[0] for tup in items]:
                sold_sum += item.value
                member.inventory.remove(item)

            member.balance += sold_sum

            embeds[-1].add_field(
                name="Selling Items",
                value=f"Sold {len(items)} items for *${sold_sum}*. Your new balance is *${member.balance}.*"
            )

        embeds.append(discord.Embed())
        embeds[-1].set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )
        embeds[-1].title = "Buy Cycle Finished"
        embeds[-1].description = f"You cycled through *{boxes_cycled}* boxes and discovered **{new_items}** new items!"

        final_embeds = []
        for embed in embeds:
            final_embeds += Utils.split_embeds(embed)

        for embed in final_embeds:
            await ctx.reply(embed=embed, mention_author=False)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.write_data()


async def setup(bot):
    await bot.add_cog(Shop(bot))
    print("Shop Cog loaded")


async def teardown(bot):
    print("Shop Cog unloaded")
    await bot.remove_cog(Shop(bot))
