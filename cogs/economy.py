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

def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy Cog loaded")

def teardown(bot):
    bot.remove_cog(Economy(bot))
    print("Economy Cog unloaded")