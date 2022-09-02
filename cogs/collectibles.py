##-----imports-----##

import discord
import random
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from definitions import Member, SharkErrors, Item, Collection, Listing, Cooldown
import commandviews

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


##-----Cog Code-----##

class Collectibles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.server = bot.get_guild(ids.server)

    @commands.Cog.listener()
    async def on_ready(self):
        self.server = await self.bot.fetch_guild(ids.server)
        print("\n")
        for collection in list(Collection.collections):
            print(f"Loaded {collection.name} collection with {len(collection.items)} items.")

    @commands.hybrid_command(aliases=["search"])
    async def item(self, ctx, *, search):
        member = Member.get(ctx.author.id)
        try:
            item = Item.search(search)
        except SharkErrors.ItemNotFoundError:
            await ctx.reply(f"Sorry, I couldn't find *{search}*!", mention_author=False)
            return
        if item.id in member.collection:
            await ctx.reply(embed=item.generate_embed(), mention_author=False)
        else:
            fakeItem = Item.FakeItem(item)
            await ctx.reply(embed=fakeItem.generate_embed(), mention_author=False)

    @commands.hybrid_command(aliases=["i", "inv"])
    async def inventory(self, ctx):
        member = Member.get(ctx.author.id)
        member.sort_inventory()

        items = {}

        for collection in Collection.collections:
            items[collection] = {}
            for item in collection.items:
                if member.inventory.count(item.id) > 0:
                    items[collection][item] = member.inventory.count(item.id)

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
            embed.description = f"Balance: ${member.get_balance()}"
            embed.set_thumbnail(url=ctx.author.avatar.url)

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
    @commands.has_role(ids.roles["Mod"])
    async def additem(self, ctx, target: discord.Member, *, search):
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except SharkErrors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        targetMember.add_to_inventory(item)
        await ctx.reply(f"Added **{item.name}** to *{target.display_name}*'s inventory.", mention_author=False)
        targetMember.upload_data()

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def removeitem(self, ctx, target: discord.Member, *, search):
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except SharkErrors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        try:
            targetMember.remove_from_inventory(item)
        except SharkErrors.ItemNotInInventoryError:
            await ctx.reply(f"Couldn't find item in *{target.display_name}*'s inventory", mention_author=False)
            return
        await ctx.reply(f"Removed **{item.name}** from *{target.display_name}*'s inventory.", mention_author=False)
        targetMember.upload_data()

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def grantall(self, ctx, *itemids):
        items = []
        for itemid in itemids:
            items.append(Item.get(itemid))

        members = Member.members.values()
        for member in members:
            member.add_items_to_inventory(items)

        await ctx.send(f"Granted {len(items)} items each to {len(members)} members.")

    @commands.command()
    async def open(self, ctx, boxType="all"):
        member = Member.get(ctx.author.id)
        boxType = boxType.lower()
        boxes = []
        if boxType == "all":
            for itemid in member.get_inventory():
                item = Item.get(itemid)
                if type(item) == Item.Lootbox:
                    boxes.append(item)
            if len(boxes) == 0:
                await ctx.send("It doesn't look like you have any lootboxes!")
                return
        else:
            try:
                item = Item.search(boxType)
            except SharkErrors.ItemNotFoundError:
                await ctx.send("I couldn't find that lootbox!")
                return
            if type(item) != Item.Lootbox:
                await ctx.send("That item isn't a lootbox!")
                return
            boxes.append(item)
        for box in boxes:
            item = box.roll()

            if box.id == "LOOT10":
                if item.id in member.get_inventory():
                    possibleItems = []
                    for possibleItem in Collection.mythic.items:
                        if possibleItem.id not in member.collection:
                            possibleItems.append(possibleItem)
                    if possibleItems:
                        while item not in possibleItems:
                            item = box.roll()

            embed = discord.Embed()
            embed.title = f"{box.name} opened!"
            if item.id in member.collection:
                embed.description = f"You got {item.rarity.icon} *{item.name}*!"
            else:
                embed.description = f"You got :sparkles: {item.rarity.icon} *{item.name}* :sparkles:!"
            embed.color = item.collection.colour
            embed.set_footer(text=item.description)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

            member.remove_from_inventory(box)
            member.add_to_inventory(item)

            await ctx.reply(embed=embed, mention_author=False)

        member.upload_data()

    @commands.hybrid_command()
    async def claim(self, ctx):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Claim All"
        embed.color = discord.Colour.blurple()
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embedText = "Free shit!"

        claimedBoxes = []

        ##--Hourly--##
        if member.cooldowns["hourly"].expired:
            member.cooldowns["hourly"].reset()
            roll = random.randint(1, 10000)
            if roll < 6500:
                lootbox = Item.get("LOOT1")
            elif roll < (6500 + 3000):
                lootbox = Item.get("LOOT2")
            elif roll < (6500 + 3000 + 400):
                lootbox = Item.get("LOOT3")
            elif roll < (6500 + 3000 + 400 + 80):
                lootbox = Item.get("LOOT4")
            elif roll < (6500 + 3000 + 400 + 80 + 15):
                lootbox = Item.get("LOOT5")
            else:
                lootbox = Item.get("LOOT10")
            if Item.currentEventBox is not None:
                roll = random.randint(1, 3)
                if roll != 3:
                    lootbox = Item.currentEventBox
            claimedBoxes.append(lootbox)
            member.add_to_inventory(lootbox)
            embed.add_field(name="Hourly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Hourly",
                            value=f"You still have {member.cooldowns['hourly'].timeremainingstr} left!",
                            inline=False)

        ##--Daily--##
        if member.cooldowns["daily"].expired:
            member.cooldowns["daily"].reset()
            roll = random.randint(1, 10000)
            if roll < 2000:
                lootbox = Item.get("LOOT2")
            elif roll < (2000 + 6500):
                lootbox = Item.get("LOOT3")
            elif roll < (2000 + 6500 + 1200):
                lootbox = Item.get("LOOT4")
            elif roll < (2000 + 6500 + 1200 + 250):
                lootbox = Item.get("LOOT5")
            else:
                lootbox = Item.get("LOOT10")
            claimedBoxes.append(lootbox)
            member.add_to_inventory(lootbox)
            embed.add_field(name="Daily",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Daily",
                            value=f"You still have {member.cooldowns['daily'].timeremainingstr} left!",
                            inline=False)

        ##--Weekly--##
        if member.cooldowns["weekly"].expired:
            member.cooldowns["weekly"].reset()
            roll = random.randint(1, 10000)
            if roll < 2000:
                lootbox = Item.get("LOOT3")
            elif roll < (2000 + 6500):
                lootbox = Item.get("LOOT4")
            elif roll < (2000 + 6500 + 1000):
                lootbox = Item.get("LOOT5")
            else:
                lootbox = Item.get("LOOT10")
            claimedBoxes.append(lootbox)
            member.add_to_inventory(lootbox)
            embed.add_field(name="Weekly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Weekly",
                            value=f"You still have {member.cooldowns['weekly'].timeremainingstr} left!",
                            inline=False)

        embed.description = embedText

        view = commandviews.ClaimView(claimedBoxes, ctx.author.id, embed)

        await ctx.reply(embed=embed, view=view)
        member.upload_data()

    @commands.hybrid_command()
    async def sell(self, ctx, *, search):
        member = Member.get(ctx.author.id)
        if search.lower() in ["dupes", "duplicates"]:
            dupeFound = False
            for itemid in member.get_inventory():
                item = Item.get(itemid)
                if item.id[:-1] == "LOOT":
                    continue
                if member.inventory.count(item.id) > 1:
                    dupeFound = True
                    for i in range(1, member.inventory.count(item.id)):
                        member.remove_from_inventory(item)
                        member.add_balance(item.get_value())
                        await ctx.reply(
                            f"You sold **{item.name}** for $*{item.get_value()}*. Your new balance is $*{member.get_balance()}*.",
                            mention_author=False)
                        member.upload_data()
            if not dupeFound:
                await ctx.reply(f"You don't have any duplicates! Nice!", mention_author=False)
            return

        if search.lower() in ["all", "*"]:
            items = 0
            amount = 0
            itemList = []
            for itemid in member.get_inventory():
                item = Item.get(itemid)
                if item.id[:-1] == "LOOT":
                    continue
                itemList.append(item)
            for item in itemList:
                items += 1
                amount += item.get_value()
                member.remove_from_inventory(item)
                member.add_balance(item.get_value())
            await ctx.reply(
                f"You sold **{items} item(s)** for $*{amount}*. Your new balance is $*{member.get_balance()}*.",
                mention_author=False)
            member.upload_data()
            return

        try:
            item = Item.search(search)
        except SharkErrors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return

        if type(item) == Item.Lootbox:
            await ctx.reply("You can't sell lootboxes!", mention_author=False)
            return

        try:
            member.remove_from_inventory(item)
            member.add_balance(item.get_value())
            await ctx.reply(
                f"You sold **{item.name}** for *${item.get_value()}*. Your new balance is $*{member.get_balance()}*.",
                mention_author=False)
            member.upload_data()
        except SharkErrors.ItemNotInInventoryError:
            await ctx.reply(f"It looks like you don't have an **{item.name}** :pensive:", mention_author=False)

    @commands.command(aliases=["c", "col"])
    async def collection(self, ctx, *args):
        member = Member.get(ctx.author.id)

        if len(args) == 0:

            ## Short Collection
            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Collection"
            embed.set_thumbnail(url=ctx.author.avatar.url)

            totalItems = 0

            for collection in Collection.collections:
                totalItems += len(collection.items)
                collectionItemsDiscovered = 0
                for item in collection.items:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1

                icon = collection.icon

                embed.add_field(name=f"{icon}  {collection.name}",
                                value=f"{collectionItemsDiscovered}/{len(collection.items)} items discovered",
                                inline=False)

            embed.description = f"{len(member.collection)}/{totalItems} items discovered"

            await ctx.reply(embed=embed, mention_author=False)
            return

        elif args[0] in ["full", "*", "all"]:

            ## Full Collection

            embeds = []
            embeds.append(discord.Embed())
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.avatar.url)

            length = 0

            for collection in Collection.collections:
                collectionItemsDiscovered = 0
                itemsList = ""
                for item in collection.items:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1
                        itemsList += f"{item.name} *({item.id})*\n"
                    else:
                        itemsList += f"??? *({item.id})*\n"

                icon = collection.icon

                length += len(itemsList)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.avatar.url)

                embeds[-1].add_field(
                    name=f"{icon}  {collection.name} ({collectionItemsDiscovered}/{len(collection.collection)})",
                    value=itemsList[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection (Page {embeds.index(embed) + 1}/{len(embeds)})"

            for embed in embeds:
                await ctx.reply(embed=embed, mention_author=False)

        else:

            ## Select Collections

            collectionsToShow = []
            for collectionName in args:
                for collection in Collection.collections:
                    if collectionName.lower() == collection.name.lower():
                        collectionsToShow.append(collection)
                        break

            if len(collectionsToShow) != len(args):
                await ctx.reply("I don't recognise all of those collection names, please try again!",
                                mention_author=False)
                return

            collectionsToShow = list(set(collectionsToShow))

            embeds = []
            embeds.append(discord.Embed())
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.avatar.url)

            length = 0

            for collection in collectionsToShow:
                collectionItemsDiscovered = 0
                itemsList = ""
                for item in collection.items:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1
                        itemsList += f"{item.name} *({item.id})*\n"
                    else:
                        itemsList += f"??? *({item.id})*\n"

                icon = collection.icon

                length += len(itemsList)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.avatar.url)

                embeds[-1].add_field(
                    name=f"{icon}  {collection.name} ({collectionItemsDiscovered}/{len(collection.items)})",
                    value=itemsList[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection (Page {embeds.index(embed) + 1}/{len(embeds)})"

            for embed in embeds:
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed()
        embed.title = "Shop"
        embed.description = "Fucking Capitalists"
        shopText = ""
        for listing in Listing.listings:
            shopText += f"{listing.item.rarity.icon} {listing.item.name} | *${listing.price}*\n"
        embed.add_field(name="**Available Items**", value=shopText)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command()
    async def buy(self, ctx, quantity: int, *, search):
        member = Member.get(ctx.author.id)
        search = search.lower()
        num = quantity
        try:
            item = Item.search(search)
        except SharkErrors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return
        if item not in Listing.availableItems:
            await ctx.reply("I'm afraid you can't buy that!", mention_author=False)
            return
        listing = discord.utils.get(Listing.listings, item=item)
        if num == "max":
            num = member.get_balance() // listing.price
        if member.get_balance() < num * listing.price or num == 0:
            await ctx.reply(
                f"I'm afraid you don't have enough to buy {item.rarity.icon} **{item.name}**",
                mention_author=False)
            return
        for i in range(num):
            member.add_balance(-1 * listing.price)
            member.add_to_inventory(item)

        embed = discord.Embed()
        embed.title = f"Bought {num}x {item.rarity.icon} {item.name}"
        embed.description = f"You bought {num}x {item.rarity.icon} {item.name} for *${listing.price * num}*"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        view = commandviews.BuyView([item] * num, ctx.author.id, embed)

        await ctx.reply(embed=embed, view=view)
        member.upload_data()

    @commands.command(aliases=["gift"])
    async def give(self, ctx, target: discord.Member, *, search):
        member = Member.get(ctx.author.id)
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except SharkErrors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return

        try:
            member.remove_from_inventory(item)
            targetMember.add_to_inventory(item)
            await ctx.reply(f"You gave {item.rarity.icon} **{item.name}** to *{target.display_name}*",
                            mention_author=False)
        except SharkErrors.ItemNotInInventoryError:
            await ctx.reply(
                f"It looks like you don't have {item.rarity.icon} **{item.name}** :pensive:",
                mention_author=False)
        member.upload_data()
        targetMember.upload_data()


##----Extension Code----##

async def setup(bot):
    await bot.add_cog(Collectibles(bot))
    print("Collectibles Cog loaded")


async def teardown(bot):
    print("Collectibles Cog unloaded")
    await bot.remove_cog(Collectibles(bot))
