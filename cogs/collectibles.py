##-----imports-----##

import discord, random
from cogs import economy
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from definitions import Member

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

inventories = {}
collections = {}
timeFormat = "%S:%M:%H/%d:%m:%Y"
cooldowns = {}
autodelete = []
shopListings = []
shopItems = []

##-----Class Defintions-----##

class Item():
    
    def __init__(self, itemData):
        self.id, self.name, self.description = itemData[0:3]
        self.rarity = Rarities.ref[itemData[3]]
        try:
            self.imageUrl = itemData[4]
        except IndexError:
            self.imageUrl = None

    def generate_embed(self):
        embed = discord.Embed()
        embed.title = self.name
        embed.color = self.rarity.colour
        embed.description = self.description
        embed.set_footer(text = f"{self.rarity.name} | {self.id}")
        if self.imageUrl != None:
            embed.set_thumbnail(url=self.imageUrl)

        return embed

class Lootbox(Item):

    def __init__(self, itemData):
        super().__init__(itemData[:-2])
        self.price = int(itemData[-2])
        self.lootPoolCode = itemData[-1]

    def roll(self):

        self.lootPool = {}
        lootPoolCodes = self.lootPoolCode
        cumulativeChance = 0
        lootCodeList = lootPoolCodes.split(";")
        for code in lootCodeList:
            codeData = code.split(":")

            collection = find_collection_by_code(codeData[0])
            itemSet = collection.collection
            cumulativeChance += int(codeData[1])
            self.lootPool[cumulativeChance] = itemSet

        d100 = random.randint(1,100)
        for chance, pool in self.lootPool.items():
            if d100 <= chance:
                return pool[random.randint(0,len(pool)-1)]

class Collection():
    
    def __init__(self, name, code, filename, lootbox=False):
        self.name = name
        self.code = code
        
        r = open(f"collectibles/{filename}", "r")
        fileData = r.read()
        r.close()

        self.collection = []
        if lootbox == False:
            for line in fileData.split("\n"):
                if line == "":
                    continue
                itemData = line.split("|")
                self.collection.append(Item(itemData))
        else:
            for line in fileData.split("\n"):
                if line == "":
                    continue
                itemData = line.split("|")
                self.collection.append(Lootbox(itemData))
                    
class Rarity():

    def __init__(self, name, colour, price):
        self.name = name
        self.colour = colour
        self.price = price
        self.icon = f"{name.lower()}_item"

    def fetch_emoji(self, server):
        self.emoji = discord.utils.get(server.emojis, name=self.icon)

class Rarities():

    common = Rarity("Common", discord.Color.light_grey(), 5)
    uncommon = Rarity("Uncommon", discord.Color.green(), 10)
    rare = Rarity("Rare", 0x6fa8dc, 20)
    legendary = Rarity("Legendary", discord.Color.dark_purple(), 50)
    exotic = Rarity("Exotic", discord.Color.gold(), 150)
    valentines = Rarity("Valentines", 0xfb00ff, 10)
    witchqueen = Rarity("Witch_Queen", 0x758B72, 10)

    ref = {
        "common" : common,
        "uncommon" : uncommon,
        "rare" : rare,
        "legendary" : legendary,
        "exotic" : exotic,
        "love" : valentines,
        "valentines" : valentines,
        "witch_queen" : witchqueen,
        "witch queen" : witchqueen}

class Collections():

    common = Collection("Common", "C", "common.txt")
    uncommon = Collection("Uncommon", "U", "uncommon.txt")
    rare = Collection("Rare", "R", "rare.txt")
    legendary = Collection("Legendary", "L", "legendary.txt")
    exotic = Collection("Exotic", "E", "exotic.txt")
    lootboxes = Collection("Lootboxes", "LOOT", "lootboxes.txt", True)
    valentines = Collection("Valentines", "LOVE", "valentines.txt")
    witchqueen = Collection("Witch_Queen", "WQ", "witch_queen.txt")

    collectionsList = [common, uncommon, rare, legendary, exotic, valentines, witchqueen, lootboxes]

class Listing():

    def __init__(self, listingData):
        self.item = search_for_item(listingData[0])
        self.price = int(listingData[1])
        shopItems.append(self.item)

##-----Functions-----##

def find_item_by_id(id):
    for collection in Collections.collectionsList:
        item = discord.utils.get(collection.collection, id=id)
        if item != None:
            return item
    raise ItemNotFound

def search_for_item(search):
    for collection in Collections.collectionsList:
        for item in collection.collection:
            if item.id == search.upper():
                return item
            elif item.name.lower() == search.lower():
                return item
    for box in Collections.lootboxes.collection:
        if box.name.lower() == search.lower() + " lootbox":
            return box
    raise ItemNotFound

def find_collection_by_code(code):
    for collection in Collections.collectionsList:
        if collection.code == code:
            return collection
    return None

def search_for_lootbox(search):
    item = discord.utils.get(Collections.lootboxes.collection, id=search.upper())
    if item != None:
        return item
    ref = {"common": "LOOT1", "uncommon" : "LOOT2", "rare" : "LOOT3", "legendary" : "LOOT4", "exotic" : "LOOT5"}
    if search in ref:
        return find_item_by_id(ref[search])
    return None

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

def add_to_collection(memberid, item):
    member = Member.get(memberid)
    member.add_to_collection(item)

def add_to_inventory(memberid, item):
    member = Member.get(memberid)
    member.add_to_inventory(item)

def remove_from_inventory(memberid, item):
    member = Member.get(memberid)
    member.remove_from_inventory(item)

def check_collection(memberid, item):
    member = Member.get(memberid)
    return (item.id in member.collection)

async def check_counting_box(message):
    roll = random.randint(1,100)
    if roll < 3:
        box = find_item_by_id("LOOT5")
    elif roll < 10:
        box = find_item_by_id("LOOT4")
    elif roll < 25:
        box = find_item_by_id("LOOT3")
    elif roll < 50:
        box = find_item_by_id("LOOT2")
    else:
        box = find_item_by_id("LOOT1")
    member = Member.get(message.author.id)
    member.add_to_inventory(box)
    await message.channel.send(f"Hey, would you look at that! You found a {box.rarity.emoji} **{box.name}**!")

async def check_event_box(message):
    member = Member(message.author.id)
    box = find_item_by_id("LOOT8")
    if box.id not in member.collection:
        member.add_to_inventory(box)
        await message.channel.send(f"Hey, would you look at that! You found a {box.rarity.emoji} **{box.name}**!")
        return True
    return False



##-----File Reading Functions-----##

def read_inventory_file():
    r = open(f"data/collectibles/inventories.txt", "r")
    fileData = r.read()
    r.close()

    inventories.clear()

    fileLines = fileData.split("\n")
    for line in fileLines:
        if line == "":
            continue
        lineData = line.split(",")
        memberitems = []
        if len(lineData) > 1:
            for itemData in lineData[1:]:
                memberitems.append(find_item_by_id(itemData))
        inventories[int(lineData[0])] = memberitems

def read_collections_file():
    r = open(f"data/collectibles/collections.txt", "r")
    fileData = r.read()
    r.close()

    collections.clear()

    fileLines = fileData.split("\n")
    for line in fileLines:
        if line == "":
            continue
        lineData = line.split(",")
        memberitems = []
        if len(lineData) > 1:
            for itemData in lineData[1:]:
                memberitems.append(find_item_by_id(itemData))
        collections[int(lineData[0])] = memberitems

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

def read_autodelete_file():
    try:
        r = open("data/collectibles/autodelete.txt", "r")
        fileData = r.read()
        r.close()
    except FileNotFoundError:
        print("autodelete.txt not found, creating!")
        w = open("data/collectibles/autodelete.txt", "w")
        w.close()
        r = open("data/collectibles/autodelete.txt", "r")
        fileData = r.read()
        r.close()
    for line in fileData.split("\n"):
        if line != "":
            autodelete.append(int(line))

def read_shop_file():
    try:
        r = open("data/collectibles/shop.txt", "r")
        fileData = r.read()
        r.close()
    except FileNotFoundError:
        print("shop.txt not found, creating!")
        w = open("data/collectibles/shop.txt", "w")
        w.close()
        r = open("data/collectibles/shop.txt", "r")
        fileData = r.read()
        r.close()
    for line in fileData.split("\n"):
        if line != "":
            shopListings.append(Listing(line.split(":")))

def load_all_files():
    read_inventory_file()
    read_collections_file()
    read_cooldowns_file()
    read_autodelete_file()
    read_shop_file()

##-----File Writing Functions-----##

def write_inventories_file():
    fileData = ""
    for member, items in inventories.items():
        fileData += str(member)
        for item in items:
            fileData += "," + item.id
        fileData += "\n"
    
    w = open(f"data/collectibles/inventories.txt", "w")
    w.write(fileData[:-1])
    w.close()

def write_collections_file():
    fileData = ""
    for member, items in collections.items():
        fileData += str(member)
        for item in items:
            fileData += "," + item.id
        fileData += "\n"
    
    w = open(f"data/collectibles/collections.txt", "w")
    w.write(fileData[:-1])
    w.close()

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

def write_autodelete_file():
    fileData = ""
    for id in autodelete:
        fileData += str(id) + "\n"
    
    w = open(f"data/collectibles/autodelete.txt", "w")
    w.write(fileData[:-1])
    w.close()

def write_shop_file():
    fileData = ""
    for listing in shopListings:
        fileData += f"{listing.item.name}:{listing.price}\n"
    
    w = open(f"data/collectibles/shop.txt", "w")
    w.write(fileData[:-1])
    w.close()

##-----Cog Code-----##
    
class Collectibles(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        server = await self.bot.fetch_guild(ids.server)
        for rarity in list(Rarities.ref.values()):
            rarity.fetch_emoji(server)
        print("\n")
        for collection in list(Collections.collectionsList):
            print(f"Loaded {collection.name} collection with {len(collection.collection)} items.")

    @commands.command(aliases=["search"])
    async def item(self, ctx, *, search):
        try:
            item = search_for_item(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return
        if check_collection(ctx.author.id, item) == True:
            await ctx.send(embed=item.generate_embed())
        else:
            fakeItem = Item([item.id, "???", "???", item.rarity.name.lower()])
            await ctx.send(embed=fakeItem.generate_embed())

    @commands.command(aliases=["i", "inv"])
    async def inventory(self, ctx):
        member = Member.get(ctx.author.id)
        invData = []
        for itemid in member.inventory:
            invData.append(find_item_by_id(itemid))

        inv = {}
        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Inventory"
        embed.description = f"Balance: ${member.balance}"
        embed.set_thumbnail(url=ctx.author.avatar_url)

        server = await self.bot.fetch_guild(ids.server)

        for collection in Collections.collectionsList:
            inv[collection] = {}
            for item in collection.collection:
                if invData.count(item) > 0:
                    inv[collection][item] = invData.count(item)
            collectionItems = ""
            for item in inv[collection]:
                collectionItems += f"{inv[collection][item]}x {item.name} *({item.id})*\n"
            emoji = discord.utils.get(server.emojis, name=collection.name.lower() + "_item")
            if inv[collection] != {}:
                embed.add_field(name = f"{emoji}  {collection.name}", value=collectionItems[:-1], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def additem(self, ctx, target : discord.Member, *, search):
        targetMember = Member.get(target.id)
        try:
            item = search_for_item(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return
        targetMember.add_to_inventory(item)
        await ctx.send(f"Added **{item.name}** to *{target.display_name}*'s inventory.")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def removeitem(self, ctx, target : discord.Member, *, search):
        try:
            item = search_for_item(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return
        try:
            remove_from_inventory(target.id, item)
        except ItemNotInInventory:
            await ctx.send(f"Couldn't find item in *{target.display_name}*'s inventory")
            return
        await ctx.send(f"Removed **{item.name}** from *{target.display_name}*'s inventory.")

    @commands.command()
    async def open(self, ctx, boxType = "all"):
        boxType = boxType.lower()
        if boxType == "all":
            boxes = []
            boxFound = False
            for item in inventories[ctx.author.id]:
                if type(item) == Lootbox:
                    boxFound = True
                    boxes.append(item)
            if boxFound == True:
                for box in boxes:
                    inventories[ctx.author.id].remove(box)
                    item = box.roll()
                
                    embed = discord.Embed()
                    embed.title = f"{box.name} opened!"
                    embed.description = f"You got {item.rarity.emoji} *{item.name}*!"
                    embed.color = item.rarity.colour
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

                    if ctx.author.id in autodelete and item in inventories[ctx.author.id]:
                        economy.add_user_balance(ctx.author.id, item.rarity.price)
                        embed.description += f"\n*(duplicate, auto-sold for ${item.rarity.price}*)"

                    else:
                        add_to_inventory(ctx.author.id, item)

                    await ctx.send(embed=embed)
            else:
                await ctx.send("It looks like you don't have any lootboxes!")
            return
        box = search_for_lootbox(boxType)
        if box == None:
            await ctx.send("I couldn't find that type of box :pensive:")
            return
        if ctx.author.id in inventories:
            try:
                inventories[ctx.author.id].remove(box)
                item = box.roll()
                add_to_inventory(ctx.author.id, item)
                
                embed = discord.Embed()
                embed.title = f"{box.name} opened!"
                embed.description = f"You got {item.rarity.emoji} *{item.name}*!"
                embed.color = item.rarity.colour
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)

            except ValueError:
                await ctx.send(f"Looks like you don't have any *{box.name}* :pensive:")
        else:
            await ctx.send(f"Looks like you don't have any *{box.name}* :pensive:")

    @commands.command()
    async def hourly(self, ctx):
        timeCheck, timeDifference = check_cooldown(ctx.author.id, 0, 60*60)
        if timeCheck == True:
            roll = random.randint(1,100)
            if roll < 85:
                lootbox = find_item_by_id("LOOT1")
            elif roll < 99:
                lootbox = find_item_by_id("LOOT2")
            else:
                lootbox = find_item_by_id("LOOT3")
            add_to_inventory(ctx.author.id, lootbox)
            await ctx.send(f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**!")
        else:
            await ctx.send(f"Slow down there! You still have {convert_td_to_string(60*60 - timeDifference)} left before you can do that.")
            
    @commands.command()
    async def daily(self, ctx):
        timeCheck, timeDifference = check_cooldown(ctx.author.id, 1, 24*60*60)
        if timeCheck == True:
            roll = random.randint(1,100)
            if roll < 85:
                lootbox = find_item_by_id("LOOT2")
            elif roll < 99:
                lootbox = find_item_by_id("LOOT3")
            else:
                lootbox = find_item_by_id("LOOT4")
            add_to_inventory(ctx.author.id, lootbox)
            await ctx.send(f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**!")
        else:
            await ctx.send(f"Slow down there! You still have {convert_td_to_string(24*60*60 - timeDifference)} left before you can do that.")
            
    @commands.command()
    async def weekly(self, ctx):
        timeCheck, timeDifference = check_cooldown(ctx.author.id, 2, 7*24*60*60)
        if timeCheck == True:
            roll = random.randint(1,100)
            if roll < 85:
                lootbox = find_item_by_id("LOOT3")
            elif roll < 99:
                lootbox = find_item_by_id("LOOT4")
            else:
                lootbox = find_item_by_id("LOOT5")
            add_to_inventory(ctx.author.id, lootbox)
            await ctx.send(f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**!")
        else:
            await ctx.send(f"Slow down there! You still have {convert_td_to_string(7*24*60*60 - timeDifference)} left before you can do that.")

    @commands.command()
    async def claim(self, ctx, cooldown = "all"):
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
                roll = random.randint(1,100)
                if roll < 85:
                    lootbox = find_item_by_id("LOOT1")
                elif roll < 99:
                    lootbox = find_item_by_id("LOOT2")
                else:
                    lootbox = find_item_by_id("LOOT3")
                add_to_inventory(ctx.author.id, lootbox)
                embedText += (f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**! *(Hourly)*\n")
            else:
                embedText += (f"You still have {convert_td_to_string(60*60 - timeDifference)} left! *(Hourly)*\n")

            ##--Daily--##
            timeCheck, timeDifference = check_cooldown(ctx.author.id, 1, 24*60*60)
            if timeCheck == True:
                roll = random.randint(1,100)
                if roll < 85:
                    lootbox = find_item_by_id("LOOT2")
                elif roll < 99:
                    lootbox = find_item_by_id("LOOT3")
                else:
                    lootbox = find_item_by_id("LOOT4")
                add_to_inventory(ctx.author.id, lootbox)
                embedText += (f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**! *(Daily)*\n")
            else:
                embedText += (f"You still have {convert_td_to_string(24*60*60 - timeDifference)} left! *(Daily)*\n")

            ##--Weekly--##
            timeCheck, timeDifference = check_cooldown(ctx.author.id, 2, 7*24*60*60)
            if timeCheck == True:
                roll = random.randint(1,100)
                if roll < 85:
                    lootbox = find_item_by_id("LOOT3")
                elif roll < 99:
                    lootbox = find_item_by_id("LOOT4")
                else:
                    lootbox = find_item_by_id("LOOT5")
                add_to_inventory(ctx.author.id, lootbox)
                embedText += (f"Success! You claimed a {lootbox.rarity.emoji} **{lootbox.name}**! *(Weekly)*")
            else:
                embedText += (f"You still have {convert_td_to_string(7*24*60*60 - timeDifference)} left! *(Weekly)*")

            embed.description = embedText
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"I'm afraid I don't understand '{cooldown}' :pensive:")

    @commands.command()
    async def sell(self, ctx, *, search):
        if search.lower() in ["dupes", "duplicates"]:
            dupeFound = False
            for item in inventories[ctx.author.id]:
                if item.id[:-1] == "LOOT":
                    continue
                if inventories[ctx.author.id].count(item) > 1:
                    dupeFound = True
                    for i in range(1, inventories[ctx.author.id].count(item)):
                        remove_from_inventory(ctx.author.id, item)
                        economy.add_user_balance(ctx.author.id, item.rarity.price)
                        await ctx.send(f"You sold **{item.name}** for $*{item.rarity.price}*. Your new balance is $*{economy.get_user_balance(ctx.author.id)}*.")
            if dupeFound == False:
                await ctx.send(f"You don't have any duplicates! Nice!")
            return

        if search.lower() in ["all", "*"]:
            items = 0
            amount = 0
            itemList = []
            for item in inventories[ctx.author.id]:
                if item.id[:-1] == "LOOT":
                    continue
                itemList.append(item)
            for item in itemList:
                items += 1
                amount += item.rarity.price
                remove_from_inventory(ctx.author.id, item)
                economy.add_user_balance(ctx.author.id, item.rarity.price)
            await ctx.send(f"You sold **{items} item(s)** for $*{amount}*. Your new balance is $*{economy.get_user_balance(ctx.author.id)}*.")
            return

        try:
            item = search_for_item(search)
        except ItemNotFound:
            await ctx.send("Sorry, I couldn't find that item!")
            return

        if type(item) == Lootbox:
            await ctx.send("You can't sell lootboxes!")
            return

        try:
            remove_from_inventory(ctx.author.id, item)
            economy.add_user_balance(ctx.author.id, item.rarity.price)
            await ctx.send(f"You sold **{item.name}** for *${item.rarity.price}*. Your new balance is $*{economy.get_user_balance(ctx.author.id)}*.")
        except ItemNotInInventory:
            await ctx.send(f"It looks like you don't have an **{item.name}** :pensive:")

    @commands.command(aliases = ["c", "col"])
    async def collection(self, ctx):
        if ctx.author.id not in collections:
            collections[ctx.author.id] = []
            write_collections_file()
        server = await self.bot.fetch_guild(ids.server)
        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Collection"
        embed.description = f"{len(collections[ctx.author.id])} items discovered."
        embed.set_thumbnail(url=ctx.author.avatar_url)
        for collection in Collections.collectionsList:
            collectionItemsDiscovered = 0
            itemsList = ""
            for item in collection.collection:
                if item in collections[ctx.author.id]:
                    collectionItemsDiscovered += 1
                    itemsList += f"{item.name} *({item.id})*\n"
                else:
                    itemsList += f"??? *({item.id})*\n"
            emoji = discord.utils.get(server.emojis, name=collection.name.lower() + "_item")
            embed.add_field(name = f"{emoji}  {collection.name} ({collectionItemsDiscovered}/{len(collection.collection)})", value=itemsList[:-1], inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases = ["ad", "autodel"])
    async def autodelete(self, ctx, value = "check"):
        value = value.lower()
        if value == "check":
            if ctx.author.id in autodelete:
                await ctx.send("You have set duplicates to automatically sell.")
            else:
                await ctx.send("You have not set duplicates to automatically sell.")
        elif value in ["on", "yes", "y", "true", "enabled"]:
            await ctx.send("Enabled automatic selling of duplicates")
            if ctx.author.id not in autodelete:
                autodelete.append(ctx.author.id)
                write_autodelete_file()
        elif value in ["off", "no", "n", "false", "disabled"]:
            await ctx.send("Disabled automatic selling of duplicates")
            if ctx.author.id in autodelete:
                autodelete.remove(ctx.author.id)
                write_autodelete_file()
        else:
            await ctx.send(f"I'm afraid I don't understand '{value}'")

    @commands.command()
    @commands.is_owner()
    async def loaddata(self, ctx):
        load_all_files()
        server = await self.bot.fetch_guild(ids.server)
        for rarity in list(Rarities.ref.values()):
            rarity.fetch_emoji(server)
        print("\n")
        for collection in list(Collections.collectionsList):
            print(f"Loaded {collection.name} collection with {len(collection.collection)} items.")
        await ctx.send("Done!")

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed()
        embed.title = "Shop"
        embed.description = "Fucking Capitalists"
        shopText = ""
        for listing in shopListings:
            shopText += (f"{listing.item.rarity.emoji} {listing.item.name} | *${listing.price}*\n")
        embed.add_field(name="**Available Items**", value=shopText)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, search):
        try:
            item = search_for_item(search)
        except ItemNotFound:
            await ctx.send("I'm afraid I couldn't find that item!")
            return
        if item not in shopItems:
            await ctx.send("I'm afraid you can't buy that!")
            return
        if economy.get_user_balance(ctx.author.id) < item.price:
            await ctx.send(f"I'm afraid you don't have enough to buy {item.rarity.emoji} **{item.name}**")
            return
        economy.add_user_balance(ctx.author.id, -1*item.price)
        add_to_inventory(ctx.author.id, item)
        embed = discord.Embed()
        embed.title = f"Bought {item.name}"
        embed.description = f"You bought {item.rarity.emoji} {item.name} for *${item.price}*"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["gift"])
    async def give(self, ctx, target : discord.Member, *, search):
        try:
            item = search_for_item(search)
        except ItemNotFound:
            await ctx.send("I'm afraid I couldn't find that item!")
            return

        try:
            remove_from_inventory(ctx.author.id, item)
            add_to_inventory(target.id, item)
            await ctx.send(f"You gave **{item.name}** to *{target.display_name}*")
        except ItemNotInInventory:
            await ctx.send(f"It looks like you don't have **{item.name}** :pensive:")


##----Extension Code----##
        
def setup(bot):
    load_all_files()
    bot.add_cog(Collectibles(bot))
    print("Collectibles Cog loaded")

def teardown(bot):
    print("Collectibles Cog unloaded")
    bot.remove_cog(Collectibles(bot))
