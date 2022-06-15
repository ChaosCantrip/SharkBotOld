##-----imports-----##

import discord, random
from cogs import economy
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from definitions import Member, SharkErrors, Item, Collection, Listing

import secret
if secret.testBot:
    import testids as ids
else:
    import ids

##-----Error Definitions-----##

class Error(Exception):
    pass

class ItemNotInInventory(Error):
    pass

class ItemNotFound(Error):
    pass

class ItemDataInvalid(Error):
    pass

class MemberInventoryNotFound(Error):

    def __init__(self, memberid):
        inventories[memberid] = []
        write_inventories_file()

        
class MemberCollectionNotFound(Error):

    def __init__(self, memberid):
        collections[memberid] = []
        write_inventories_file()

##-----Data Definitions-----##

timeFormat = "%S:%M:%H/%d:%m:%Y"
cooldowns = {}

##-----Functions-----##

def check_cooldown(memberid, cooldownid, timer):
    if memberid not in cooldowns:
        dtnow = datetime.now()
        dthourly = dtnow - timedelta(hours = 2)
        dtdaily = dtnow - timedelta(days = 2)
        dtweekly = dtnow - timedelta(days = 8)
        cooldowns[memberid] = [dthourly, dtdaily, dtweekly]

    timeDifference = (datetime.now() - cooldowns[memberid][cooldownid]).total_seconds()
    if timeDifference > timer:
        cooldowns[memberid][cooldownid] = datetime.now()
        write_cooldowns_file()
        return True, timeDifference
    else:
        return False, timeDifference

def convert_td_to_string(td):
    seconds = int(td)
    days, seconds = seconds // (24*60*60), seconds % (24*60*60)
    hours, seconds = seconds // (60*60), seconds % (60*60)
    minutes, seconds = seconds // 60, seconds % 60

    outputString = ""
    if days != 0:
        if days == 1:
            outputString += f"{days} day, "
        else:
            outputString += f"{days} days, "
    if hours != 0:
        if hours == 1:
            outputString += f"{hours} hour, "
        else:
            outputString += f"{hours} hours, "
    if minutes != 0:
        if minutes == 1:
            outputString += f"{minutes} minute, "
        else:
            outputString += f"{minutes} minutes, "
    if outputString == "":
        if seconds == 1:
            outputString += f"{seconds} second "
        else:
            outputString += f"{seconds} seconds "
    else:
        outputString = outputString[:-2] + f" and {seconds} "
        if seconds == 1:
            outputString += f"second "
        else:
            outputString += f"seconds "
    return outputString

async def check_counting_box(message):
    roll = random.randint(1,100)
    if roll < 3:
        box = Item.get("LOOT5")
    elif roll < 10:
        box = Item.get("LOOT4")
    elif roll < 25:
        box = Item.get("LOOT3")
    elif roll < 50:
        box = Item.get("LOOT2")
    else:
        box = Item.get("LOOT1")
    member = Member.get(message.author.id)
    member.add_to_inventory(box)
    await message.channel.send(f"Hey, would you look at that! You found a {box.rarity.emoji} **{box.name}**!")

async def check_event_box(message):
    member = Member.get(message.author.id)
    box = Item.get("LOOT9")
    if box.id not in member.collection:
        member.add_to_inventory(box)
        await message.channel.send(f"Hey, would you look at that! You found a {box.rarity.emoji} **{box.name}**!")
        return True
    return False



##-----File Reading Functions-----##

def read_cooldowns_file():
    r = open(f"data/collectibles/cooldowns.txt", "r")
    fileData = r.read()
    r.close()

    cooldowns.clear()

    fileLines = fileData.split("\n")
    for line in fileLines:
        if line == "":
            continue
        lineData = line.split("|")
        memberStr, hourlyStr, dailyStr, weeklyStr = lineData
        hourlyObj = datetime.strptime(hourlyStr, timeFormat)
        dailyObj = datetime.strptime(dailyStr, timeFormat)
        weeklyObj = datetime.strptime(weeklyStr, timeFormat)
        cooldowns[int(memberStr)] = [hourlyObj, dailyObj, weeklyObj]

def load_all_files():
    read_cooldowns_file()

##-----File Writing Functions-----##

def write_cooldowns_file():
    fileData = ""
    for member, datetimes in cooldowns.items():
        fileData += str(member)
        for dt in datetimes:
            fileData += "|" + dt.strftime(timeFormat)
        fileData += "\n"
    
    w = open(f"data/collectibles/cooldowns.txt", "w")
    w.write(fileData[:-1])
    w.close()

##-----Cog Code-----##
    
class Collectibles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        server = await self.bot.fetch_guild(ids.server)
        print("\n")
        for collection in list(Collection.collections):
            print(f"Loaded {collection.name} collection with {len(collection.items)} items.")

    @commands.command(aliases=["search"])
    async def item(self, ctx, *, search):
        member = Member.get(ctx.author.id)
        try:
            item = Item.search(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return
        if item.id in member.collection == True:
            await ctx.send(embed=item.generate_embed())
        else:
            fakeItem = Item([item.id, "???", "???", item.rarity.name.lower()])
            await ctx.send(embed=fakeItem.generate_embed())

    @commands.command(aliases=["i", "inv"])
    async def inventory(self, ctx):
        member = Member.get(ctx.author.id)
        server = await self.bot.fetch_guild(ids.server)

        items = {}

        for collection in Collections.collectionsList:
            items[collection] = {}
            for item in collection.collection:
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
            embed.set_thumbnail(url=ctx.author.avatar_url)

            for collectionData in data:
                collection = collectionData[0]
                collectionItems = collectionData[1]

                emoji = discord.utils.get(server.emojis, name=collection.name.lower() + "_item")
                embed.add_field(name = f"{emoji}  {collection.name}", value=collectionItems, inline=True)

            embeds.append(embed)

        for embed in embeds:
            if len(embeds) > 1:
                embed.title = f"{ctx.author.display_name}'s Inventory (Page {embeds.index(embed)+1}/{len(embeds)})"
            else:
                embed.title = f"{ctx.author.display_name}'s Inventory"
            await ctx.send(embed=embed)



    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def additem(self, ctx, target : discord.Member, *, search):
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return
        targetMember.add_to_inventory(item)
        await ctx.send(f"Added **{item.name}** to *{target.display_name}*'s inventory.")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def removeitem(self, ctx, target : discord.Member, *, search):
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return
        try:
            targetMember.remove_from_inventory(item)
        except SharkErrors.ItemNotInInventoryError:
            await ctx.send(f"Couldn't find item in *{target.display_name}*'s inventory")
            return
        await ctx.send(f"Removed **{item.name}** from *{target.display_name}*'s inventory.")

    @commands.command()
    async def open(self, ctx, boxType = "all"):
        member = Member.get(ctx.author.id)
        boxType = boxType.lower()
        if boxType == "all":
            boxes = []
            boxFound = False
            for itemid in member.inventory:
                item = Item.get(itemid)
                if type(item) == Lootbox:
                    boxFound = True
                    boxes.append(item)
            if boxFound == True:
                for box in boxes:
                    member.remove_from_inventory(box)
                    item = box.roll()

                    if box.id == "LOOT10":
                        if item.id in member.inventory:
                            possibleItems = []
                            for possibleItem in Collections.mythic.collection:
                                if possibleItem.id not in member.collection:
                                    possibleItems.append(possibleItem)
                            if possibleItems != []:
                                while item not in possibleItems:
                                    item = box.roll()
                
                    embed = discord.Embed()
                    embed.title = f"{box.name} opened!"
                    if item.id in member.collection:
                        embed.description = f"You got {item.rarity.emoji} *{item.name}*!"
                    else:
                        embed.description = f"You got :sparkles: {item.rarity.emoji} *{item.name}* :sparkles:!"
                    embed.color = item.rarity.colour
                    embed.set_footer(text=item.description)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    
                    member.add_to_inventory(item)

                    await ctx.send(embed=embed)
            else:
                await ctx.send("It looks like you don't have any lootboxes!")
            return
        box = Item.search(boxType)
        if box == None:
            await ctx.send("I couldn't find that type of box :pensive:")
            return
        try:
            member.remove_from_inventory(box)
            item = box.roll()

            if box.id == "LOOT10":
                if item.id in member.inventory:
                    possibleItems = []
                    for possibleItem in Collections.mythic.collection:
                        if possibleItem.id not in member.collection:
                            possibleItems.append(possibleItem)
                    if possibleItems != []:
                        while item not in possibleItems:
                            item = box.roll()
                
            embed = discord.Embed()
            embed.title = f"{box.name} opened!"
            if item.id in member.collection:
                embed.description = f"You got {item.rarity.emoji} *{item.name}*!"
            else:
                embed.description = f"You got :sparkles: {item.rarity.emoji} *{item.name}* :sparkles:!"
            embed.color = item.rarity.colour
            embed.set_footer(text=item.description)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

            member.add_to_inventory(item)

            await ctx.send(embed=embed)

        except SharkErrors.ItemNotInInventoryError:
            await ctx.send(f"Looks like you don't have any *{box.name}* :pensive:")

    @commands.command()
    async def hourly(self, ctx):
        member = Member.get(ctx.author.id)
        timeCheck, timeDifference = check_cooldown(ctx.author.id, 0, 60*60)
        if timeCheck == True:
            roll = random.randint(1,10000)
            if roll < 6500:
                lootbox = Item.get("LOOT1")
            elif roll < (6500+3000):
                lootbox = Item.get("LOOT2")
            elif roll < (6500+3000+400):
                lootbox = Item.get("LOOT3")
            elif roll < (6500+3000+400+80):
                lootbox = Item.get("LOOT4")
            elif roll < (6500+3000+400+80+15):
                lootbox = Item.get("LOOT5")
            else:
                lootbox = Item.get("LOOT10")
            member.add_to_inventory(lootbox)
            await ctx.send(f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**!")
        else:
            await ctx.send(f"Slow down there! You still have {convert_td_to_string(60*60 - timeDifference)} left before you can do that.")
            
    @commands.command()
    async def daily(self, ctx):
        member = Member.get(ctx.author.id)
        timeCheck, timeDifference = check_cooldown(ctx.author.id, 1, 24*60*60)
        if timeCheck == True:
            roll = random.randint(1,10000)
            if roll < 2000:
                lootbox = Item.get("LOOT2")
            elif roll < (2000+6500):
                lootbox = Item.get("LOOT3")
            elif roll < (2000+6500+1200):
                lootbox = Item.get("LOOT4")
            elif roll < (2000+6500+1200+250):
                lootbox = Item.get("LOOT5")
            else:
                lootbox = Item.get("LOOT10")
            member.add_to_inventory(lootbox)
            await ctx.send(f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**!")
        else:
            await ctx.send(f"Slow down there! You still have {convert_td_to_string(24*60*60 - timeDifference)} left before you can do that.")
            
    @commands.command()
    async def weekly(self, ctx):
        member = Member.get(ctx.author.id)
        timeCheck, timeDifference = check_cooldown(ctx.author.id, 2, 7*24*60*60)
        if timeCheck == True:
            roll = random.randint(1,10000)
            if roll < 2000:
                lootbox = Item.get("LOOT3")
            elif roll < (2000+6500):
                lootbox = Item.get("LOOT4")
            elif roll < (2000+6500+1000):
                lootbox = Item.get("LOOT5")
            else:
                lootbox = Item.get("LOOT10")
            member.add_to_inventory(lootbox)
            await ctx.send(f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**!")
        else:
            await ctx.send(f"Slow down there! You still have {convert_td_to_string(7*24*60*60 - timeDifference)} left before you can do that.")

    @commands.command()
    async def claim(self, ctx, cooldown = "all"):
        member = Member.get(ctx.author.id)
        cooldown = cooldown.lower()
        if cooldown in ["hour", "hourly", "h"]:
            await ctx.invoke(self.bot.get_command('hourly'))
        elif cooldown in ["day", "daily", "d"]:
            await ctx.invoke(self.bot.get_command('daily'))
        elif cooldown in ["week", "weekly", "w"]:
            await ctx.invoke(self.bot.get_command('weekly'))
        elif cooldown in ["*", "all"]:
            embed = discord.Embed()
            embed.title = "Claim All"
            embed.color = discord.Colour.blurple()
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embedText = ""
            
            ##--Hourly--##
            timeCheck, timeDifference = check_cooldown(ctx.author.id, 0, 60*60)
            if timeCheck == True:
                roll = random.randint(1,10000)
                if roll < 6500:
                    lootbox = Item.get("LOOT1")
                elif roll < (6500+3000):
                    lootbox = Item.get("LOOT2")
                elif roll < (6500+3000+400):
                    lootbox = Item.get("LOOT3")
                elif roll < (6500+3000+400+80):
                    lootbox = Item.get("LOOT4")
                elif roll < (6500+3000+400+80+15):
                    lootbox = Item.get("LOOT5")
                else:
                    lootbox = Item.get("LOOT10")
                member.add_to_inventory(lootbox)
                embedText += (f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**! *(Hourly)*\n")
            else:
                embedText += (f"You still have {convert_td_to_string(60*60 - timeDifference)} left! *(Hourly)*\n")

            ##--Daily--##
            timeCheck, timeDifference = check_cooldown(ctx.author.id, 1, 24*60*60)
            if timeCheck == True:
                roll = random.randint(1,10000)
                if roll < 2000:
                    lootbox = Item.get("LOOT2")
                elif roll < (2000+6500):
                    lootbox = Item.get("LOOT3")
                elif roll < (2000+6500+1200):
                    lootbox = Item.get("LOOT4")
                elif roll < (2000+6500+1200+250):
                    lootbox = Item.get("LOOT5")
                else:
                    lootbox = Item.get("LOOT10")
                member.add_to_inventory(lootbox)
                embedText += (f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**! *(Daily)*\n")
            else:
                embedText += (f"You still have {convert_td_to_string(24*60*60 - timeDifference)} left! *(Daily)*\n")

            ##--Weekly--##
            timeCheck, timeDifference = check_cooldown(ctx.author.id, 2, 7*24*60*60)
            if timeCheck == True:
                roll = random.randint(1,10000)
                if roll < 2000:
                    lootbox = Item.get("LOOT3")
                elif roll < (2000+6500):
                    lootbox = Item.get("LOOT4")
                elif roll < (2000+6500+1000):
                    lootbox = Item.get("LOOT5")
                else:
                    lootbox = Item.get("LOOT10")
                member.add_to_inventory(lootbox)
                embedText += (f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**! *(Weekly)*")
            else:
                embedText += (f"You still have {convert_td_to_string(7*24*60*60 - timeDifference)} left! *(Weekly)*")

            embed.description = embedText
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"I'm afraid I don't understand '{cooldown}' :pensive:")

    @commands.command()
    async def sell(self, ctx, *, search):
        member = Member.get(ctx.author.id)
        if search.lower() in ["dupes", "duplicates"]:
            dupeFound = False
            for itemid in member.inventory:
                item = Item.get(itemid)
                if item.id[:-1] == "LOOT":
                    continue
                if inventories[ctx.author.id].count(item) > 1:
                    dupeFound = True
                    for i in range(1, member.inventory.count(item.id)):
                        member.remove_from_inventory(item)
                        member.add_balance(item.rarity.price)
                        await ctx.send(f"You sold **{item.name}** for $*{item.rarity.price}*. Your new balance is $*{member.get_balance()}*.")
            if dupeFound == False:
                await ctx.send(f"You don't have any duplicates! Nice!")
            return

        if search.lower() in ["all", "*"]:
            items = 0
            amount = 0
            itemList = []
            for itemid in member.inventory:
                item = Item.get(itemid)
                if item.id[:-1] == "LOOT":
                    continue
                itemList.append(item)
            for item in itemList:
                items += 1
                amount += item.rarity.price
                member.remove_from_inventory(item)
                member.add_balance(item.rarity.price)
            await ctx.send(f"You sold **{items} item(s)** for $*{amount}*. Your new balance is $*{member.get_balance()}*.")
            return

        try:
            item = Item.search(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return

        if type(item) == Lootbox:
            await ctx.send("You can't sell lootboxes!")
            return

        try:
            member.remove_from_inventory(item)
            member.add_balance(item.rarity.price)
            await ctx.send(f"You sold **{item.name}** for *${item.rarity.price}*. Your new balance is $*{member.get_balance()}.")
        except SharkErrors.ItemNotInInventoryError:
            await ctx.send(f"It looks like you don't have an **{item.name}** :pensive:")

    @commands.command(aliases = ["c", "col"])
    async def collection(self, ctx, *args):
        member = Member.get(ctx.author.id)
        server = await self.bot.fetch_guild(ids.server)

        if len(args) == 0:

            ## Short Collection
            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Collection"
            embed.set_thumbnail(url=ctx.author.avatar_url)

            totalItems = 0

            for collection in Collections.collectionsList:
                totalItems += len(collection.collection)
                collectionItemsDiscovered = 0
                for item in collection.collection:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1

                emoji = discord.utils.get(server.emojis, name=collection.name.lower() + "_item")

                embed.add_field(name = f"{emoji}  {collection.name}", value= f"{collectionItemsDiscovered}/{len(collection.collection)} items discovered", inline=False)

            embed.description = f"{len(member.collection)}/{totalItems} items discovered"
            
            await ctx.send(embed=embed)
            return
        
        elif args[0] in ["full", "*", "all"]:

            ## Full Collection

            embeds = []
            embeds.append(discord.Embed())
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.avatar_url)

            length = 0

            for collection in Collections.collectionsList:
                collectionItemsDiscovered = 0
                itemsList = ""
                for item in collection.collection:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1
                        itemsList += f"{item.name} *({item.id})*\n"
                    else:
                        itemsList += f"??? *({item.id})*\n"
                emoji = discord.utils.get(server.emojis, name=collection.name.lower() + "_item")

                length += len(itemsList)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.avatar_url)

                embeds[-1].add_field(name = f"{emoji}  {collection.name} ({collectionItemsDiscovered}/{len(collection.collection)})", value=itemsList[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection (Page {embeds.index(embed)+1}/{len(embeds)})"

            for embed in embeds:
                await ctx.send(embed=embed)

        else:

            ## Select Collections

            collectionsToShow = []
            for collectionName in args:
                for collection in Collections.collectionsList:
                    if collectionName.lower() == collection.name.lower():
                        collectionsToShow.append(collection)
                        break

            if len(collectionsToShow) != len(args):
                await ctx.send("I don't recognise all of those collection names, please try again!")
                return

            collectionsToShow = list(set(collectionsToShow))

            embeds = []
            embeds.append(discord.Embed())
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.avatar_url)

            length = 0

            for collection in collectionsToShow:
                collectionItemsDiscovered = 0
                itemsList = ""
                for item in collection.collection:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1
                        itemsList += f"{item.name} *({item.id})*\n"
                    else:
                        itemsList += f"??? *({item.id})*\n"
                emoji = discord.utils.get(server.emojis, name=collection.name.lower() + "_item")

                length += len(itemsList)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.avatar_url)

                embeds[-1].add_field(name = f"{emoji}  {collection.name} ({collectionItemsDiscovered}/{len(collection.collection)})", value=itemsList[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection (Page {embeds.index(embed)+1}/{len(embeds)})"

            for embed in embeds:
                await ctx.send(embed=embed)
                

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed()
        embed.title = "Shop"
        embed.description = "Fucking Capitalists"
        shopText = ""
        for listing in Listing.listings:
            icon = await listing.item.collection.get_icon(self.bot)
            shopText += (f"{icon} {listing.item.name} | *${listing.price}*\n")
        embed.add_field(name="**Available Items**", value=shopText)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, search):
        member = Member.get(ctx.author.id)
        search = search.lower()
        splitSearch = search.split(" ")
        try:
            num = int(splitSearch[-1])
            search = " ".join(splitSearch[:-1])
        except ValueError:
            if splitSearch[-1] in ["*", "max"]:
                num = "max"
                search = " ".join(splitSearch[:-1])
            else:
                num = 1
        try:
            item = Item.search(search)
        except ItemNotFound:
            await ctx.send("I'm afraid I couldn't find that item!")
            return
        if item not in Listing.listings:
            await ctx.send("I'm afraid you can't buy that!")
            return
        if num == "max":
            num = member.get_balance() // item.price
        if member.get_balance() < num * item.price or num == 0:
            await ctx.send(f"I'm afraid you don't have enough to buy {item.rarity.emoji} **{item.name}**")
            return
        for i in range(num):
            member.add_balance(-1*item.price)
            member.add_to_inventory(item)
        embed = discord.Embed()
        embed.title = f"Bought {num}x {item.name}"
        embed.description = f"You bought {num}x {item.rarity.emoji} {item.name} for *${item.price * num}*"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["gift"])
    async def give(self, ctx, target : discord.Member, *, search):
        member = Member.get(ctx.author.id)
        targetMember = Member.get(target.id)
        try:
            item = Item.search(search)
        except ItemNotFound:
            await ctx.send("I'm afraid I couldn't find that item!")
            return

        try:
            member.remove_from_inventory(item)
            targetMember.add_to_inventory(item)
            await ctx.send(f"You gave **{item.name}** to *{target.display_name}*")
        except SharkErrors.ItemNotInInventoryError:
            await ctx.send(f"It looks like you don't have **{item.name}** :pensive:")


##----Extension Code----##
        
def setup(bot):
    load_all_files()
    bot.add_cog(Collectibles(bot))
    print("Collectibles Cog loaded")

def teardown(bot):
    print("Collectibles Cog unloaded")
    bot.remove_cog(Collectibles(bot))
