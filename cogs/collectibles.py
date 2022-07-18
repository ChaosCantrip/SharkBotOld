##-----imports-----##

import discord, random
from cogs import economy
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from definitions import Member, SharkErrors, Item, Collection, Listing
from handlers import databaseHandler

import secret
if secret.testBot:
    import testids as ids
else:
    import ids

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
        self.server = bot.get_guild(ids.server)



    @commands.Cog.listener()
    async def on_ready(self):
        self.server = await self.bot.fetch_guild(ids.server)
        print("\n")
        for collection in list(Collection.collections):
            print(f"Loaded {collection.name} collection with {len(collection.items)} items.")



    @commands.command(aliases=["search"])
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



    @commands.command(aliases=["i", "inv"])
    async def inventory(self, ctx):
        member = Member.get(ctx.author.id)

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
                
                embed.add_field(name = f"{collection.get_icon(self.server)}  {collection.name}", value=collectionItems, inline=True)

            embeds.append(embed)

        for embed in embeds:
            if len(embeds) > 1:
                embed.title = f"{ctx.author.display_name}'s Inventory (Page {embeds.index(embed)+1}/{len(embeds)})"
            else:
                embed.title = f"{ctx.author.display_name}'s Inventory"
            await ctx.reply(embed=embed, mention_author=False)



    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def additem(self, ctx, target : discord.Member, *, search):
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
    async def removeitem(self, ctx, target : discord.Member, *, search):
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

        members = Member.get_all_members()
        for member in members:
            member.add_items_to_inventory(items)

        await ctx.send(f"Granted {len(items)} items each to {len(members)} members.")
        databaseHandler.upload_all_members()


    @commands.command()
    async def open(self, ctx, boxType = "all"):
        member = Member.get(ctx.author.id)
        boxType = boxType.lower()
        if boxType == "all":
            boxes = []
            boxFound = False
            for itemid in member.inventory:
                item = Item.get(itemid)
                if type(item) == Item.Lootbox:
                    boxFound = True
                    boxes.append(item)
            if boxFound == True:
                for box in boxes:
                    member.remove_from_inventory(box)
                    item = box.roll()

                    if box.id == "LOOT10":
                        if item.id in member.inventory:
                            possibleItems = []
                            for possibleItem in Collection.mythic.items:
                                if possibleItem.id not in member.collection:
                                    possibleItems.append(possibleItem)
                            if possibleItems != []:
                                while item not in possibleItems:
                                    item = box.roll()
                
                    embed = discord.Embed()
                    embed.title = f"{box.name} opened!"
                    if item.id in member.collection:
                        embed.description = f"You got {item.rarity.get_icon(self.server)} *{item.name}*!"
                    else:
                        embed.description = f"You got :sparkles: {item.rarity.get_icon(self.server)} *{item.name}* :sparkles:!"
                    embed.color = item.collection.colour
                    embed.set_footer(text=item.description)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    
                    member.add_to_inventory(item)

                    await ctx.reply(embed=embed, mention_author=False)
            else:
                await ctx.reply("It looks like you don't have any lootboxes!", mention_author=False)
            member.upload_data()
            return
        box = Item.search(boxType)
        if box == None:
            await ctx.reply("I couldn't find that type of box :pensive:", mention_author=False)
            return
        try:
            member.remove_from_inventory(box)
            item = box.roll()

            if box.id == "LOOT10":
                if item.id in member.inventory:
                    possibleItems = []
                    for possibleItem in Collection.mythic.items:
                        if possibleItem.id not in member.collection:
                            possibleItems.append(possibleItem)
                    if possibleItems != []:
                        while item not in possibleItems:
                            item = box.roll()
                
            embed = discord.Embed()
            embed.title = f"{box.name} opened!"
            if item.id in member.collection:
                embed.description = f"You got {item.rarity.get_icon(self.server)} *{item.name}*!"
            else:
                embed.description = f"You got :sparkles: {item.rarity.get_icon(self.server)} *{item.name}* :sparkles:!"
            embed.color = item.rarity.colour
            embed.set_footer(text=item.description)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

            member.add_to_inventory(item)

            await ctx.reply(embed=embed, mention_author=False)
            member.upload_data()

        except SharkErrors.ItemNotInInventoryError:
            await ctx.reply(f"Looks like you don't have any *{box.name}* :pensive:", mention_author=False)


    @commands.command()
    async def claim(self, ctx):
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Claim All"
        embed.color = discord.Colour.blurple()
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embedText = "Free shit!"
            
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
            if Item.currentEventBox != None:
                roll = random.randint(1,3)
                if roll != 3:
                    lootbox = Item.currentEventBox
            member.add_to_inventory(lootbox)
            embed.add_field(name="Hourly", value = f"Success! You claimed a {lootbox.rarity.get_icon(self.server)} **{lootbox.name}**!", inline = False)
        else:
            embed.add_field(name="Hourly", value = f"You still have {convert_td_to_string(60*60 - timeDifference)} left!", inline = False)

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
            embed.add_field(name="Daily", value = f"Success! You claimed a {lootbox.rarity.get_icon(self.server)} **{lootbox.name}**!", inline = False)
        else:
            embed.add_field(name="Daily", value = f"You still have {convert_td_to_string(24*60*60 - timeDifference)} left!", inline = False)

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
            embed.add_field(name="Weekly", value = f"Success! You claimed a {lootbox.rarity.get_icon(self.server)} **{lootbox.name}**!", inline = False)
        else:
            embed.add_field(name="Weekly", value = f"You still have {convert_td_to_string(7*24*60*60 - timeDifference)} left!", inline = False)

        embed.description = embedText
        await ctx.reply(embed=embed, mention_author=False)
        member.upload_data()



    @commands.command()
    async def sell(self, ctx, *, search):
        member = Member.get(ctx.author.id)
        if search.lower() in ["dupes", "duplicates"]:
            dupeFound = False
            for itemid in member.inventory:
                item = Item.get(itemid)
                if item.id[:-1] == "LOOT":
                    continue
                if member.inventory.count(item.id) > 1:
                    dupeFound = True
                    for i in range(1, member.inventory.count(item.id)):
                        member.remove_from_inventory(item)
                        member.add_balance(item.rarity.value)
                        await ctx.reply(f"You sold **{item.name}** for $*{item.rarity.value}*. Your new balance is $*{member.get_balance()}*.", mention_author=False)
            if dupeFound == False:
                await ctx.reply(f"You don't have any duplicates! Nice!", mention_author=False)
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
                amount += item.rarity.value
                member.remove_from_inventory(item)
                member.add_balance(item.rarity.value)
            await ctx.reply(f"You sold **{items} item(s)** for $*{amount}*. Your new balance is $*{member.get_balance()}*.", mention_author=False)
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
            member.add_balance(item.rarity.price)
            await ctx.reply(f"You sold **{item.name}** for *${item.rarity.price}*. Your new balance is $*{member.get_balance()}.", mention_author=False)
        except SharkErrors.ItemNotInInventoryError:
            await ctx.reply(f"It looks like you don't have an **{item.name}** :pensive:", mention_author=False)
        member.upload_data()



    @commands.command(aliases = ["c", "col"])
    async def collection(self, ctx, *args):
        member = Member.get(ctx.author.id)

        if len(args) == 0:

            ## Short Collection
            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Collection"
            embed.set_thumbnail(url=ctx.author.avatar_url)

            totalItems = 0

            for collection in Collection.collections:
                totalItems += len(collection.items)
                collectionItemsDiscovered = 0
                for item in collection.items:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1

                icon = collection.get_icon(self.server)

                embed.add_field(name = f"{icon}  {collection.name}", value= f"{collectionItemsDiscovered}/{len(collection.items)} items discovered", inline=False)

            embed.description = f"{len(member.collection)}/{totalItems} items discovered"
            
            await ctx.reply(embed=embed, mention_author=False)
            return
        
        elif args[0] in ["full", "*", "all"]:

            ## Full Collection

            embeds = []
            embeds.append(discord.Embed())
            embeds[0].title = f"{ctx.author.display_name}'s Collection"
            embeds[0].description = f"{len(member.collection)} items discovered."
            embeds[0].set_thumbnail(url=ctx.author.avatar_url)

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
                
                icon = collection.get_icon(self.server)

                length += len(itemsList)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.avatar_url)

                embeds[-1].add_field(name = f"{icon}  {collection.name} ({collectionItemsDiscovered}/{len(collection.collection)})", value=itemsList[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection (Page {embeds.index(embed)+1}/{len(embeds)})"

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
                await ctx.reply("I don't recognise all of those collection names, please try again!", mention_author=False)
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
                for item in collection.items:
                    if item.id in member.collection:
                        collectionItemsDiscovered += 1
                        itemsList += f"{item.name} *({item.id})*\n"
                    else:
                        itemsList += f"??? *({item.id})*\n"
                
                icon = collection.get_icon(self.server)

                length += len(itemsList)
                if length > 5000:
                    length -= 5000
                    embeds.append(discord.Embed())
                    embeds[-1].title = f"{ctx.author.display_name}'s Collection"
                    embeds[-1].description = f"{len(member.collection)} items discovered."
                    embeds[-1].set_thumbnail(url=ctx.author.avatar_url)

                embeds[-1].add_field(name = f"{icon}  {collection.name} ({collectionItemsDiscovered}/{len(collection.items)})", value=itemsList[:-1], inline=True)

            if len(embeds) > 1:
                for embed in embeds:
                    embed.title = f"{ctx.author.display_name}'s Collection (Page {embeds.index(embed)+1}/{len(embeds)})"

            for embed in embeds:
                await ctx.reply(embed=embed, mention_author=False)
                


    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed()
        embed.title = "Shop"
        embed.description = "Fucking Capitalists"
        shopText = ""
        for listing in Listing.listings:
            shopText += (f"{listing.item.rarity.get_icon(self.server)} {listing.item.name} | *${listing.price}*\n")
        embed.add_field(name="**Available Items**", value=shopText)
        await ctx.reply(embed=embed, mention_author=False)



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
            await ctx.reply(f"I'm afraid you don't have enough to buy {item.rarity.get_icon(self.server)} **{item.name}**", mention_author=False)
            return
        for i in range(num):
            member.add_balance(-1*listing.price)
            member.add_to_inventory(item)
        embed = discord.Embed()
        embed.title = f"Bought {num}x {item.rarity.get_icon(self.server)} {item.name}"
        embed.description = f"You bought {num}x {item.rarity.get_icon(self.server)} {item.name} for *${listing.price * num}*"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)
        member.upload_data()



    @commands.command(aliases=["gift"])
    async def give(self, ctx, target : discord.Member, *, search):
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
            await ctx.reply(f"You gave {item.rarity.get_icon(self.server)} **{item.name}** to *{target.display_name}*", mention_author=False)
        except SharkErrors.ItemNotInInventoryError:
            await ctx.reply(f"It looks like you don't have {item.rarity.get_icon(self.server)} **{item.name}** :pensive:", mention_author=False)
        member.upload_data()
        targetMember.upload_data()


##----Extension Code----##
        
def setup(bot):
    load_all_files()
    bot.add_cog(Collectibles(bot))
    print("Collectibles Cog loaded")

def teardown(bot):
    print("Collectibles Cog unloaded")
    bot.remove_cog(Collectibles(bot))
