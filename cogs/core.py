import discord
from discord.ext import commands
import datetime

import secret
if secret.testBot:
    import testids as ids
else:
    import ids

class Core(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, message):
        await message.channel.send(f"Pong! t={(datetime.datetime.now() - message.message.created_at).total_seconds() * 1000}ms")

def setup(bot):
    bot.add_cog(Core(bot))