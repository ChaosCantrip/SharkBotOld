import discord
from discord.ext import commands

import secret
if secret.testBot:
    import testids as ids
else:
    import ids



class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    def read_econ(self):
        r = open("econ.txt", "r")
        fileData = r.read()
        r.close()

        split1 = fileData.split(";")
        split2 = {}
        for item in split1:
            split = item.split(":")
            split2[int(split[0])] = int(split[1])

        return split2

    def write_econ(self, data):
        fileData = ""
        for account in data:
            fileData = fileData + f"{int(account)}:{int(data[account])};"
        fileData = fileData[:-1]

        w = open("econ.txt", "w")
        w.write(fileData)
        w.close()

    def get_user_balance(self, id):
        data = self.read_econ()
        print(data)
        try:
            return data[id]
        except:
            data[id] = 0
            self.write_econ(data)
            return data[id]

    def set_user_balance(self, id, balance):
        data = self.read_econ()
        data[id] = balance
        self.write_econ(data)

    def add_user_balance(self, id, amount):
        data = self.read_econ()
        data[id] = data[id] + amount
        self.write_econ(data)

    @commands.command(aliases=["setbalance", "setbal"])
    @commands.has_role(ids.roles["Mod"])
    async def set_balance(self, ctx, account, amount):
        id = int(account[3:-1])
        self.set_user_balance(id, int(amount))
        user = await self.bot.fetch_user(int(account[3:-1]))
        await ctx.send(f"Set {user.display_name}'s balance to {amount}.")

    @commands.command(aliases=["addbalance", "addbal"])
    @commands.has_role(ids.roles["Mod"])
    async def add_balance(self, ctx, account, amount):
        id = int(account[3:-1])
        self.add_user_balance(id, int(amount))
        user = await self.bot.fetch_user(int(account[3:-1]))
        await ctx.send(f"{amount} added to {user.display_name}'s account.")

    @commands.command(aliases=["getbalance", "getbal"])
    async def get_balance(self, ctx, account):
        bal = self.get_user_balance(int(account[3:-1]))
        user = await self.bot.fetch_user(int(account[3:-1]))
        await ctx.send(f"{user.display_name}'s balance is: {bal}")

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, mode="get", account="self", amount=0):
        if account == "self":
            account = f"!@<{ctx.author.id}>"
        else:
            try:
                id = int(id[3:-1])
            except:
                await ctx.send("Unrecognised user ID")
                return

        account = await self.bot.fetch_user(int(account[3:-1]))
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
        






def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy Cog loaded")

def teardown(bot):
    print("Economy Cog unloaded")
    bot.remove_cog(Economy(bot))
