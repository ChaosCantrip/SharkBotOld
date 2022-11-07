import discord
from discord.ext import commands, tasks

import random

from SharkBot import Item, Member, Views


class Lootbox(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        description="Claim Hourly, Daily and Weekly rewards."
    )
    async def claim(self, ctx: commands.Context) -> None:
        member = Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Claim All"
        embed.colour = discord.Colour.blurple()
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed_text = "Free shit!"

        claimed_boxes = []

        if member.cooldowns["hourly"].expired:  # Hourly Claim
            member.cooldowns["hourly"].reset()
            roll = random.randint(1, 10000)
            if roll < 6500:
                lootbox = Item.get("LOOTC")
            elif roll < (6500 + 3000):
                lootbox = Item.get("LOOTU")
            elif roll < (6500 + 3000 + 400):
                lootbox = Item.get("LOOTR")
            elif roll < (6500 + 3000 + 400 + 80):
                lootbox = Item.get("LOOTL")
            elif roll < (6500 + 3000 + 400 + 80 + 15):
                lootbox = Item.get("LOOTE")
            else:
                lootbox = Item.get("LOOTM")
            if Item.currentEventBox is not None:
                roll = random.randint(1, 3)
                if roll != 3:
                    lootbox = Item.currentEventBox
            claimed_boxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Hourly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Hourly",
                            value=f"You still have {member.cooldowns['hourly'].time_remaining_string} left!",
                            inline=False)

        if member.cooldowns["daily"].expired:  # Daily Claim
            member.cooldowns["daily"].reset()
            roll = random.randint(1, 10000)
            if roll < 2000:
                lootbox = Item.get("LOOTU")
            elif roll < (2000 + 6500):
                lootbox = Item.get("LOOTR")
            elif roll < (2000 + 6500 + 1200):
                lootbox = Item.get("LOOTL")
            elif roll < (2000 + 6500 + 1200 + 250):
                lootbox = Item.get("LOOTE")
            else:
                lootbox = Item.get("LOOTM")
            claimed_boxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Daily",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Daily",
                            value=f"You still have {member.cooldowns['daily'].time_remaining_string} left!",
                            inline=False)

        if member.cooldowns["weekly"].expired:  # Weekly Claim
            member.cooldowns["weekly"].reset()
            roll = random.randint(1, 10000)
            if roll < 2000:
                lootbox = Item.get("LOOTR")
            elif roll < (2000 + 6500):
                lootbox = Item.get("LOOTL")
            elif roll < (2000 + 6500 + 1000):
                lootbox = Item.get("LOOTE")
            else:
                lootbox = Item.get("LOOTM")
            claimed_boxes.append(lootbox)
            member.inventory.add(lootbox)
            embed.add_field(name="Weekly",
                            value=f"Success! You claimed a {lootbox.rarity.icon} **{lootbox.name}**!",
                            inline=False)
        else:
            embed.add_field(name="Weekly",
                            value=f"You still have {member.cooldowns['weekly'].time_remaining_string} left!",
                            inline=False)

        embed.description = embed_text

        if len(claimed_boxes) > 0:
            view = Views.ClaimView(claimed_boxes, ctx.author.id, embed) if claimed_boxes else None
            view.message = await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            await ctx.reply(embed=embed, mention_author=False)

        if claimed_boxes:
            await member.missions.log_action("claim", ctx)
            member.stats.claims += 1
            member.stats.claimedBoxes += len(claimed_boxes)

        member.write_data()


async def setup(bot):
    await bot.add_cog(Lootbox(bot))
    print("Lootbox Cog loaded")


async def teardown(bot):
    print("Lootbox Cog unloaded")
    await bot.remove_cog(Lootbox(bot))
