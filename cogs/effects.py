import discord
from discord.ext import tasks, commands

import SharkBot

class Effects(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def effects(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Effects"
        embed.set_thumbnail(
            url=ctx.author.display_avatar.url
        )
        effects = member.effects.details
        if len(effects) > 0:
            embed.description = f"You have `{len(effects)}` effects active."
            for effect in effects:
                embed.add_field(
                    name=effect[0],
                    value=effect[1],
                    inline=False
                )
        else:
            embed.description = "You have no active effects."

        for e in SharkBot.Utils.split_embeds(embed):
            await ctx.reply(embed=e, mention_author=False)


class _UseHandler:

    @staticmethod
    async def use_loaded_dice(member: SharkBot.Member.Member, num: int, embed: discord.Embed):
        member.effects.add("Loaded Dice", charges=num)
        embed.description = f"You now have `{member.effects.get('Loaded Dice').charges}x` Active"

    @staticmethod
    async def use_binder(member: SharkBot.Member.Member, embed: discord.Embed):
        embed.description = "You used a Binder. Fuck you, I haven't implemented that yet."

    @staticmethod
    async def use_god_binder(member: SharkBot.Member.Member, embed: discord.Embed):
        embed.description = "You used a God's Binder. Fuck you, I haven't implemented that yet."


async def setup(bot):
    await bot.add_cog(Effects(bot))
    print("Effects Cog loaded")


async def teardown(bot):
    print("Effects Cog unloaded")
    await bot.remove_cog(Effects(bot))