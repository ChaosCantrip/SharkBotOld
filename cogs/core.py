from inspect import currentframe
import discord
from discord.ext import tasks, commands
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
    async def ping(self, ctx):
        await ctx.send("Pong!")



    @commands.command()
    async def pingtime(self, ctx):
        await ctx.send(f"Pong! t={(datetime.datetime.now() - ctx.message.created_at).total_seconds() * 1000}ms")



    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, text):
        await channel.send(text)

    @commands.command()
    async def paypal(self, ctx):
        await ctx.send("https://paypal.me/chaoscantrip")

    @commands.command()
    @commands.has_role(ids.roles["Mod"])
    async def migrate(self, ctx, *, newChannel: discord.VoiceChannel):
        currentChannel = ctx.author.voice.channel
        members = list(currentChannel.members)
        for member in members:
            await member.move_to(newChannel)

    @commands.command()
    async def countdown(self, ctx):
        now = datetime.datetime.now()
        raidtime = datetime.datetime(2022, 3, 5, 18)
        timediff = raidtime - now
        td = timediff.total_seconds()

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
        
        embed = discord.Embed()
        embed.title = "Vow of The Disciple Raid Countdown"
        embed.description = f"{outputString} until the raid race begins!"
        embed.color = 0x758B72
        try:
            embed.set_thumbnail(url="https://i.pinimg.com/originals/87/93/bc/8793bc836dabd48ae51381b7c43e74dd.jpg")
        except:
            pass
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Core(bot))
    print("Core Cog loaded")



def teardown(bot):
    print("Core Cog unloaded")
    bot.remove_cog(Core(bot))