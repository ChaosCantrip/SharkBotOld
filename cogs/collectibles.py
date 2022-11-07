import random

import discord
from discord.ext import commands

from SharkBot import Member, Errors, Item, Collection, Views, IDs, Utils


class Collectibles(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(aliases=["search"])
    async def item(self, ctx: commands.Context, *, search: str) -> None:
        member = Member.get(ctx.author.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply(f"Sorry, I couldn't find *{search}*!", mention_author=False)
            return
        if member.collection.contains(item):
            await ctx.reply(embed=item.embed, mention_author=False)
        else:
            fake_item = Item.FakeItem(item)
            await ctx.reply(embed=fake_item.embed, mention_author=False)

    @commands.hybrid_command(aliases=["i", "inv"])
    async def inventory(self, ctx: commands.Context) -> None:
        member = Member.get(ctx.author.id)
        member.inventory.sort()

        items = {}

        for collection in Collection.collections:
            items[collection] = {}
            for item in collection.items:
                if member.inventory.items.count(item) > 0:
                    items[collection][item] = member.inventory.items.count(item)

        collections_to_remove = []
        for collection in items:
            if len(items[collection]) == 0:
                collections_to_remove.append(collection)

        for collection in collections_to_remove:
            items.pop(collection)

        raw_embed_data = []

        for collection in items:
            collection_data = ""
            for item in items[collection]:
                collection_data += f"{items[collection][item]}x {item.name} *({item.id})*\n"
                if len(collection_data) > 1000:
                    raw_embed_data.append([collection, collection_data[:-1]])
                    collection_data = ""

            if collection_data != "":
                raw_embed_data.append([collection, collection_data[:-1]])

        embed_data = [[]]

        embed_length = 0
        for data in raw_embed_data:
            if embed_length + len(data[1]) > 5000:
                embed_data.append([])
                embed_length = 0
            embed_data[-1].append(data)
            embed_length += len(data[1])

        embeds = []

        for data in embed_data:
            embed = discord.Embed()
            embed.description = f"Balance: ${member.balance}"
            embed.set_thumbnail(url=ctx.author.display_avatar.url)

            for collection_data in data:
                collection = collection_data[0]
                collection_items = collection_data[1]

                embed.add_field(name=f"{collection.icon}  {collection.name}", value=collection_items,
                                inline=True)

            embeds.append(embed)

        for embed in embeds:
            if len(embeds) > 1:
                embed.title = f"{ctx.author.display_name}'s Inventory (Page {embeds.index(embed) + 1}/{len(embeds)})"
            else:
                embed.title = f"{ctx.author.display_name}'s Inventory"
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def additem(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        target_member = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        target_member.inventory.add(item)
        await ctx.reply(f"Added **{item.name}** to *{target.display_name}*'s inventory.", mention_author=False)
        target_member.write_data()

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def removeitem(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        target_member = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        try:
            target_member.inventory.remove(item)
        except Errors.ItemNotInInventoryError:
            await ctx.reply(f"Couldn't find item in *{target.display_name}*'s inventory", mention_author=False)
            return
        await ctx.reply(f"Removed **{item.name}** from *{target.display_name}*'s inventory.", mention_author=False)
        target_member.write_data()

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def grantall(self, ctx: commands.Context, *itemids: str) -> None:
        items = [Item.get(itemid) for itemid in itemids]

        members = Member.members.values()
        for member in members:
            for item in items:
                member.inventory.add(item)
        await ctx.send(f"Granted {[item.name for item in items]} each to {len(members)} members.")

        for member in members:
            member.write_data()

    @commands.command()
    async def open(self, ctx: commands.Context, box_type: str = "all") -> None:
        member = Member.get(ctx.author.id)
        member.inventory.sort()

        if box_type.lower() in ["all", "*"]:  # $open all
            boxes = member.inventory.lootboxes
            if len(boxes) == 0:
                await ctx.reply("It doesn't look like you have any lootboxes!", mention_author=False)
                return
        else:  # $open specific lootbox
            box = Item.search(box_type)
            if type(box) != Item.Lootbox:
                await ctx.send(f"**{str(box)}** isn't a Lootbox!", mention_author=False)
                return
            if not member.inventory.contains(box):
                await ctx.send(f"I'm afraid you don't have any **{box}**!", mention_author=False)
                return
            boxes = [box]

        embed = discord.Embed()
        embed.title = "Open Boxes"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        boxes_dict = {}
        for box in boxes:
            boxes_dict[box] = boxes_dict.get(box, 0) + 1

        box_sets = [[box] * qty for box, qty in boxes_dict.items()]

        for box_set in box_sets:
            opened_box = box_set[0]
            for i in range(0, len(box_set), 10):
                result = member.inventory.open_boxes([(box, False) for box in box_set[i:i+10]])

                embed.add_field(
                    name=f"Opened {len(result)}x {str(opened_box)}",
                    value="\n".join(
                        [f"{str(item)}{' :sparkles:' if new_item else ''}" for item, new_item in result]
                    )
                )

        embeds = Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed)

        member.write_data()

    @commands.hybrid_command(
        description="Claim Hourly, Daily and Weekly rewards."
    )
    async def claim(self, ctx: commands.Context) -> None:
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Claim All"
        embed.colour = discord.Colour.blurple()
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed_text = "Free shit!"

        claimed_boxes = []

        if member.cooldowns["hourly"].expired:  # Hourly Claim
            member.cooldowns["hourly"].reset()
            roll = random.randint(1, 10000)
            if roll < 6500:
                lootbox = Item.get("LOOTC")
            elif roll < (6500 + 3000):
                lootbox = Item.get("LOOTU")
            elif roll < (6500 + 3000 + 400):
                lootbox = Item.get("LOOTR")
            elif roll < (6500 + 3000 + 400 + 80):
                lootbox = Item.get("LOOTL")
            elif roll < (6500 + 3000 + 400 + 80 + 15):
                lootbox = Item.get("LOOTE")
            else:
                lootbox = Item.get("LOOTM")
            if Item.currentEventBox is not None:
                roll = random.randint(1, 3)
                if roll != 3:
                    lootbox = Item.currentEventBox
            claimed_boxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Hourly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Hourly",
                            value=f"You still have {member.cooldowns['hourly'].time_remaining_string} left!",
                            inline=False)

        if member.cooldowns["daily"].expired:  # Daily Claim
            member.cooldowns["daily"].reset()
            roll = random.randint(1, 10000)
            if roll < 2000:
                lootbox = Item.get("LOOTU")
            elif roll < (2000 + 6500):
                lootbox = Item.get("LOOTR")
            elif roll < (2000 + 6500 + 1200):
                lootbox = Item.get("LOOTL")
            elif roll < (2000 + 6500 + 1200 + 250):
                lootbox = Item.get("LOOTE")
            else:
                lootbox = Item.get("LOOTM")
            claimed_boxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Daily",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Daily",
                            value=f"You still have {member.cooldowns['daily'].time_remaining_string} left!",
                            inline=False)

        if member.cooldowns["weekly"].expired:  # Weekly Claim
            member.cooldowns["weekly"].reset()
            roll = random.randint(1, 10000)
            if roll < 2000:
                lootbox = Item.get("LOOTR")
            elif roll < (2000 + 6500):
                lootbox = Item.get("LOOTL")
            elif roll < (2000 + 6500 + 1000):
                lootbox = Item.get("LOOTE")
            else:
                lootbox = Item.get("LOOTM")
            claimed_boxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Weekly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Weekly",
                            value=f"You still have {member.cooldowns['weekly'].time_remaining_string} left!",
                            inline=False)

        embed.description = embed_text

        if len(claimed_boxes) > 0:
            view = Views.ClaimView(claimed_boxes, ctx.author.id, embed) if claimed_boxes else None
            view.message = await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            await ctx.reply(embed=embed, mention_author=False)

        if claimed_boxes:
            await member.missions.log_action("claim", ctx)
            member.stats.claims += 1
            member.stats.claimedBoxes += len(claimed_boxes)

        member.write_data()

    @commands.hybrid_command()
    async def sell(self, ctx: commands.Context, *, search: str) -> None:
        search = search.upper()

        member = Member.get(ctx.author.id)

        if search in ["ALL", "*"]:
            items = member.inventory.sellable_items
            if len(items) == 0:
                await ctx.reply("It looks like you don't have any items to sell!", mention_author=False)
                return
        elif search in ["DUPES", "D"]:
            items = [item for item in member.inventory.get_duplicates()]
            if len(items) == 0:
                await ctx.reply("It looks like you don't have any dupes! Nice!", mention_author=False)
                return
        else:
            item = Item.search(search)
            if not item.sellable:
                await ctx.reply(f"You can't sell **{item}**!", mention_author=False)
                return
            if not member.inventory.contains(item):
                await ctx.reply(f"It looks like you don't have **{item}** to sell!", mention_author=False)
                return
            else:
                items = [item]

        sold_value = 0
        for item in items:
            try:
                member.inventory.remove(item)
                sold_value += item.value
            except Errors.ItemNotInInventoryError:
                items.remove(item)

        member.balance += sold_value
        await ctx.reply(f"Sold `{len(items)} items` for **${sold_value}**.", mention_author=False)

        member.write_data()

    @commands.command(aliases=["c", "col"])
    async def collection(self, ctx: commands.Context, *args: str) -> None:
        member = Member.get(ctx.author.id)

        if len(args) == 0:  # Collections Overview

            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Collection"
            embed.set_thumbnail(url=ctx.author.display_avatar.url)

            total_items = 0

            for collection in Collection.collections:
                total_items += len(collection.items)
                collection_items_discovered = 0
                for item in collection.items:
                    if member.collection.contains(item):
                        collection_items_discovered += 1

                embed.add_field(name=f"{collection}",
                                value=f"{collection_items_discovered}/{len(collection)} items discovered",
                                inline=False)

            embed.description = f"{len(member.collection.items)}/{total_items} items discovered"

            await ctx.reply(embed=embed, mention_author=False)
            return

        elif args[0] in ["full", "*", "all"]:  # Full Collections Format

            embeds = [discord.Embed()]
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection.items)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.display_avatar.url)

            length = 0

            for collection in Collection.collections:
                collection_items_discovered = 0
                items_text = ""
                for item in collection.items:
                    if member.collection.contains(item):
                        collection_items_discovered += 1
                        items_text += f"{item.name} *({item.id})*\n"
                    else:
                        items_text += f"??? *({item.id})*\n"

                icon = collection.icon

                length += len(items_text)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection.items)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.display_avatar.url)

                embeds[-1].add_field(
                    name=f"{icon}  {collection.name} ({collection_items_discovered}/{len(collection.collection)})",
                    value=items_text[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection ({embeds.index(embed) + 1}/{len(embeds)})"

            for embed in embeds:
                await ctx.reply(embed=embed, mention_author=False)

        else:  # Specific Collections Format

            collections_to_show = []
            for collectionName in args:
                for collection in Collection.collections:
                    if collectionName.lower() == collection.name.lower() or collectionName.upper() == collection.id:
                        collections_to_show.append(collection)
                        break

            if len(collections_to_show) != len(args):
                await ctx.reply("I don't recognise all of those collection names, please try again!",
                                mention_author=False)
                return

            collections_to_show = list(set(collections_to_show))

            embeds = [discord.Embed()]
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection.items)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.display_avatar.url)

            length = 0

            for collection in collections_to_show:
                collection_items_discovered = 0
                items_text = ""
                for item in collection.items:
                    if member.collection.contains(item):
                        collection_items_discovered += 1
                        items_text += f"{item.name} *({item.id})*\n"
                    else:
                        items_text += f"??? *({item.id})*\n"

                icon = collection.icon

                length += len(items_text)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection.items)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.display_avatar.url)

                embeds[-1].add_field(
                    name=f"{icon}  {collection.name} ({collection_items_discovered}/{len(collection.items)})",
                    value=items_text[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection ({embeds.index(embed) + 1}/{len(embeds)})"

            for embed in embeds:
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["gift"])
    async def give(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        member = Member.get(ctx.author.id)
        target_member = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return

        try:
            member.inventory.remove(item)
            target_member.inventory.add(item)
            await ctx.reply(f"You gave {item.rarity.icon} **{item.name}** to *{target.display_name}*",
                            mention_author=False)
        except Errors.ItemNotInInventoryError:
            await ctx.reply(
                f"It looks like you don't have {item.rarity.icon} **{item.name}** :pensive:",
                mention_author=False)
        member.write_data()

        target_member.write_data()


async def setup(bot):
    await bot.add_cog(Collectibles(bot))
    print("Collectibles Cog loaded")


async def teardown(bot):
    print("Collectibles Cog unloaded")
    await bot.remove_cog(Collectibles(bot))
