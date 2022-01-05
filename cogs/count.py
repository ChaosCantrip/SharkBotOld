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
        


    @commands.command()
    async def check_list(self, message):
    
        countChannel = self.bot.get_channel(ids.channels["Count"])
        listChannel = self.bot.get_channel(ids.channels["People who count"])
    
        allCounts = await countChannel.history(limit=None).flatten()
        counters = []
    
        for counter in await listChannel.history(limit=None).flatten():
            counters.append(counter.content)
    
        for count in allCounts:
            authorMention = "<@!" + str(count.author.id) + ">"
            if count.author.id not in ids.blacklist and authorMention not in counters:
                counters.append(authorMention)
                await listChannel.send(authorMention)



def setup(bot):
    bot.add_cog(Count(bot))