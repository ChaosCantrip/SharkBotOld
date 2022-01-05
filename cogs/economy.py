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
            return None

    def set_user_balance(self, id, balance):
        data = self.read_econ()
        data[id] = balance
        self.write_econ(data)

    def add_user_balance(self, id, amount):
        data = self.read_econ()
        data[id] = data[id] + amount
        self.write_econ(data)

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def setbalance(self, ctx, account, amount):
        id = int(account[3:-1])
        self.set_user_balance(id, int(amount))

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def addbalance(self, ctx, account, amount):
        id = int(account[3:-1])
        self.add_user_balance(id, int(amount))

    @commands.command()
    async def balance(self, ctx):
        bal = self.get_user_balance(ctx.author.id)
        await ctx.send(f"Your balance is: {bal}")

    @commands.command()
    async def getbalance(self, ctx, account):
        bal = self.get_user_balance(int(account[3:-1]))
        user = self.bot.fetch_user(int(account[3:-1]))
        await ctx.send(f"{user.display_name}'s balance is: {bal}")
        






def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy Cog loaded")

def teardown(bot):
    print("Economy Cog unloaded")
    bot.remove_cog(Economy(bot))
