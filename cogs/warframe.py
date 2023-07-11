import discord
from discord.ext import tasks, commands

import SharkBot


class Warframe(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group()
    async def warframe(self, ctx: commands.Context) -> None:
        await ctx.send_help(self.warframe)

    @warframe.command()
    async def landscapes(self, ctx: commands.Context) -> None:
        world_state = await SharkBot.Warframe.WorldState.get_current()
        earth_cycle, cetus_cycle, vallis_cycle, cambion_cycle = world_state.landscapes
        embed = discord.Embed(title="Landscapes", color=discord.Color.orange())
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/warframe/images/3/32/OstronSyndicateFlag.png")
        embed.add_field(
            name=f"Earth | {earth_cycle.state.capitalize()}",
            value=f"Changes {discord.utils.format_dt(earth_cycle.expiry, style='R')}",
            inline=False
        )
        embed.add_field(
            name=f"Cetus | {cetus_cycle.state.capitalize()}",
            value=f"Changes {discord.utils.format_dt(cetus_cycle.expiry, style='R')}",
            inline=False
        )
        embed.add_field(
            name=f"Orb Vallis | {vallis_cycle.state.capitalize()}",
            value=f"Changes {discord.utils.format_dt(vallis_cycle.expiry, style='R')}",
            inline=False
        )
        embed.add_field(
            name=f"Cambion Drift | {cambion_cycle.state.capitalize()}",
            value=f"Changes {discord.utils.format_dt(cambion_cycle.expiry, style='R')}",
            inline=False
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Warframe(bot))
    print("Warframe Cog loaded")


async def teardown(bot):
    print("Warframe Cog unloaded")
    await bot.remove_cog(Warframe(bot))
