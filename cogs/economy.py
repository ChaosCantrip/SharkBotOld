import discord
from discord.ext import tasks, commands
from asyncio import TimeoutError

import secret
if secret.testBot:
    import testids as ids
else:
    import ids
    


def read_econ():
    r = open("econ.txt", "r")
    fileData = r.read()
    r.close()

    split1 = fileData.split(";")
    split2 = {}
    for item in split1:
        split = item.split(":")
        split2[int(split[0])] = int(split[1])

    return split2



def write_econ(data):
    fileData = ""
    for account in data:
        fileData = fileData + f"{int(account)}:{int(data[account])};"
    fileData = fileData[:-1]

    w = open("econ.txt", "w")
    w.write(fileData)
    w.close()



def get_user_balance(id):
    data = read_econ()
    print(data)
    try:
        return data[id]
    except:
        data[id] = 0
        write_econ(data)
        return data[id]



def set_user_balance(id, balance):
    data = read_econ()
    data[id] = balance
    write_econ(data)



def add_user_balance(id, amount):
    data = read_econ()
    data[id] = data[id] + amount
    write_econ(data)


class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(aliases=["setbalance", "setbal"])
    @commands.has_role(ids.roles["Mod"])
    async def set_balance(self, ctx, account, amount):
        try:
            id = int(account[3:-1])
            user = await self.bot.fetch_user(id)
        except:
            await ctx.send("Please enter a valid user to set funds for.")
            return

        try:
            amount = int(amount)
        except:
            await ctx.send("Please enter a valid number of funds to add.")
            return

        self.set_user_balance(id, amount)
        await ctx.send(f"Set {user.display_name}'s balance to {amount}.")



    @commands.command(aliases=["addbalance", "addbal", "addfunds"])
    @commands.has_role(ids.roles["Mod"])
    async def add_balance(self, ctx, account, amount):
        try:
            id = int(account[3:-1])
            user = await self.bot.fetch_user(id)
        except:
            await ctx.send("Please enter a valid user to add funds to.")
            return

        try:
            amount = int(amount)
        except:
            await ctx.send("Please enter a valid number of funds to add.")
            return

        self.add_user_balance(id, amount)
        await ctx.send(f"{amount} added to {user.display_name}'s account.")



    @commands.command(aliases=["getbalance", "getbal"])
    async def get_balance(self, ctx, account):
        try:
            id = int(account[3:-1])
            user = await self.bot.fetch_user(id)
        except:
            await ctx.send("Please enter a valid user to add funds to.")
            return

        bal = get_user_balance(id)
        await ctx.send(f"{user.display_name}'s balance is: {bal}")



    @commands.command(aliases=["bal", "econ"])
    async def balance(self, ctx, mode="get", account="self", amount=0):
        if account == "self":
            account = f"<@!{ctx.author.id}>"
        elif account[:3] != "<@!":
            amount = account
            account = f"<@!{ctx.author.id}>"

        try:
            if mode[:3] == "<@!":
                account = mode
                mode = "get"
        except:
            await ctx.send("Sorry, I didn't understand")

        mode = mode.lower()

        if mode == "get":
            await ctx.invoke(self.bot.get_command("get_balance"), account = account)
            return
        elif mode == "set":
            await ctx.invoke(self.bot.get_command("set_balance"), account = account, amount=amount)
            return
        elif mode == "add":
            await ctx.invoke(self.bot.get_command("add_balance"), account = account, amount=amount)
            return
        else:
            await ctx.send("Sorry, I didn't understand")
            return


    @commands.command(aliases=["transfer"])
    async def pay(self, ctx, target: discord.Member, amount: int):

        if get_user_balance(ctx.author.id) < amount:
            await ctx.send("Sorry, you don't have enough coins to do that.")

        message = await ctx.send(f"Transfer {amount} to {account.display_name}?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda reaction, user: user == ctx.author and reaction.message == message and reaction.emoji in ["✅", "❌"]

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except TimeoutError:
            await message.edit(content="Transfer cancelled, timed out.")
            return

        if reaction.emoji == "✅":
            add_user_balance(ctx.author.id, -amount)
            add_user_balance(target.id, amount)
            await message.edit(content=f"Transferred {amount} to {account.display_name}.")
        else:
            await message.edit(content="Transfer cancelled.")
        






def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy Cog loaded")

def teardown(bot):
    print("Economy Cog unloaded")
    bot.remove_cog(Economy(bot))
