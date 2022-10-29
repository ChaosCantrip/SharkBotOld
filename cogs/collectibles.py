import random

import discord
from discord.ext import commands

from SharkBot import Member, Errors, Item, Collection, Views, IDs


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
            fakeItem = Item.FakeItem(item)
            await ctx.reply(embed=fakeItem.embed, mention_author=False)

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

        collectionsToRemove = []
        for collection in items:
            if len(items[collection]) == 0:
                collectionsToRemove.append(collection)

        for collection in collectionsToRemove:
            items.pop(collection)

        rawEmbedData = []

        for collection in items:
            collectionData = ""
            for item in items[collection]:
                collectionData += f"{items[collection][item]}x {item.name} *({item.id})*\n"
                if len(collectionData) > 1000:
                    rawEmbedData.append([collection, collectionData[:-1]])
                    collectionData = ""

            if collectionData != "":
                rawEmbedData.append([collection, collectionData[:-1]])

        embedData = [[]]

        embedLength = 0
        for data in rawEmbedData:
            if embedLength + len(data[1]) > 5000:
                embedData.append([])
                embedLength = 0
            embedData[-1].append(data)
            embedLength += len(data[1])

        embeds = []

        for data in embedData:
            embed = discord.Embed()
            embed.description = f"Balance: ${member.balance}"
            embed.set_thumbnail(url=ctx.author.display_avatar.url)

            for collectionData in data:
                collection = collectionData[0]
                collectionItems = collectionData[1]

                embed.add_field(name=f"{collection.icon}  {collection.name}", value=collectionItems,
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
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        targetMember.inventory.add(item)
        await ctx.reply(f"Added **{item.name}** to *{target.display_name}*'s inventory.", mention_author=False)
        targetMember.write_data()

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def removeitem(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        try:
            targetMember.inventory.remove(item)
        except Errors.ItemNotInInventoryError:
            await ctx.reply(f"Couldn't find item in *{target.display_name}*'s inventory", mention_author=False)
            return
        await ctx.reply(f"Removed **{item.name}** from *{target.display_name}*'s inventory.", mention_author=False)
        targetMember.write_data()

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
    async def open(self, ctx: commands.Context, boxType: str = "all") -> None:
        member = Member.get(ctx.author.id)

        if boxType.lower() in ["all", "*"]:  # $open all
            boxes = member.inventory.lootboxes
            if len(boxes) == 0:
                await ctx.reply("It doesn't look like you have any lootboxes!", mention_author=False)
                return
        else:  # $open specific lootbox
            try:
                box = Item.search(boxType)
            except Errors.ItemNotFoundError:
                await ctx.send("I couldn't find that lootbox!", mention_author=False)
                return
            if type(box) != Item.Lootbox:
                await ctx.send("That item isn't a lootbox!", mention_author=False)
                return
            if not member.inventory.contains(box):
                await ctx.send(f"I'm afraid you don't have a {box.text}", mention_author=False)
                return
            boxes = [box]

        openedData: list[list[Item.Item, Item.Lootbox, bool]] = []

        for box in boxes:
            item = box.roll()

            if box.id == "LOOTM":  # Force Mythic Lootbox to guarantee new item
                if member.collection.contains(item):
                    possibleItems = [item for item in Collection.mythic.items if not member.collection.contains(item)]
                    if len(possibleItems) > 0:
                        item = random.choice(possibleItems)

            openedData.append([box, item, not member.collection.contains(item)])

            member.inventory.remove(box)
            member.inventory.add(item)
            member.stats.openedBoxes += 1

        member.write_data()

        for box, item, newItem in openedData:
            embed = discord.Embed()
            embed.title = f"{box.name} opened!"
            if newItem:
                embed.description = f"You got :sparkles: *{item}* :sparkles:!"
            else:
                embed.description = f"You got *{item}*!"
            embed.colour = item.collection.colour
            embed.set_footer(text=item.description)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

            await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(
        description="Claim Hourly, Daily and Weekly rewards."
    )
    async def claim(self, ctx: commands.Context) -> None:
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Claim All"
        embed.colour = discord.Colour.blurple()
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embedText = "Free shit!"

        claimedBoxes = []

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
            claimedBoxes.append(lootbox)
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
            claimedBoxes.append(lootbox)
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
            claimedBoxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Weekly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Weekly",
                            value=f"You still have {member.cooldowns['weekly'].time_remaining_string} left!",
                            inline=False)

        embed.description = embedText

        if len(claimedBoxes) > 0:
            view = Views.ClaimView(claimedBoxes, ctx.author.id, embed) if claimedBoxes else None
            view.message = await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            await ctx.reply(embed=embed, mention_author=False)

        if claimedBoxes:
            await member.missions.log_action("claim", ctx)
            member.stats.claims += 1
            member.stats.claimedBoxes += len(claimedBoxes)

        member.write_data()

    @commands.hybrid_command()
    async def sell(self, ctx: commands.Context, *, search: str) -> None:
        search = search.upper()

        member = Member.get(ctx.author.id)

        if search in ["ALL", "*"]:
            items = [item for item in member.inventory.items if type(item) == Item.Item]
            if len(items) == 0:
                await ctx.reply("It looks like you don't have any items to sell!", mention_author=False)
                return
        elif search in ["DUPES", "D"]:
            items = [item for item in member.inventory.get_duplicates() if type(item) == Item.Item]
            if len(items) == 0:
                await ctx.reply("It looks like you don't have any dupes! Nice!", mention_author=False)
                return
        else:
            item = Item.search(search)
            if type(Item) == Item.Item:
                await ctx.reply(f"You can't sell **{item}**!", mention_author=False)
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
                                value=f"{collection_items_discovered}/{len(collection.items)} items discovered",
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
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return

        try:
            member.inventory.remove(item)
            targetMember.inventory.add(item)
            await ctx.reply(f"You gave {item.rarity.icon} **{item.name}** to *{target.display_name}*",
                            mention_author=False)
        except Errors.ItemNotInInventoryError:
            await ctx.reply(
                f"It looks like you don't have {item.rarity.icon} **{item.name}** :pensive:",
                mention_author=False)
        member.write_data()

        targetMember.write_data()


async def setup(bot):
    await bot.add_cog(Collectibles(bot))
    print("Collectibles Cog loaded")


async def teardown(bot):
    print("Collectibles Cog unloaded")
    await bot.remove_cog(Collectibles(bot))
