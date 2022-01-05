import discord
from discord.ext import commands

import secret
if secret.testBot:
    import testids as ids
else:
    import ids

class Count(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Count(bot))