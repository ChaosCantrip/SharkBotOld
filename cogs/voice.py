import discord
from discord.ext import tasks, commands

import secret

if secret.testBot:
    import testids as ids
else:
    import ids


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Voice(bot))
    print("Voice Cog loaded")


async def teardown(bot):
    print("Voice Cog unloaded")
    await bot.remove_cog(Voice(bot))
