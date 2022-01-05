import discord
from discord.ext import commands

import secret
if secret.testBot:
    import testids as ids
else:
    import ids



def convert_to_num(message):

    result = ""

    for char in message.content:
        if char.isdigit():
            result = result + char

    if(result == ""):
        return None
    else:
        return int(result)



def sort_tally_table(table):
    n = len(table)

    for i in range(n):
        already_sorted = True

        for j in range (n - i - 1):
            if table[j][1] < table[j+1][1]:
                table[j], table[j+1] = table[j+1], table[j]
                already_sorted = False
        if already_sorted:
            break
    return table



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