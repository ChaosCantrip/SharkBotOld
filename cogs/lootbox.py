import discord
from discord.ext import commands, tasks

import random

from SharkBot import Item, Member, Views, Utils, Lootpool


class Lootbox(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx: commands.Context, box_type: str = "all") -> None:
        member = Member.get(ctx.author.id)
        member.inventory.sort()

        if box_type.lower() in ["all", "*"]:  # $open all
            boxes = member.inventory.unlocked_lootboxes
            if len(boxes) == 0:
                await ctx.reply("It doesn't look like you have any lootboxes you can open!", mention_author=False)
                return
        else:  # $open specific lootbox
            box = Item.search(box_type)
            if box.type != "Lootbox":
                await ctx.send(f"**{str(box)}** isn't a Lootbox!", mention_author=False)
                return
            if not member.inventory.contains(box):
                await ctx.send(f"I'm afraid you don't have any **{box}**!", mention_author=False)
                return
            if not box.unlocked:
                await ctx.send(f"That lootbox is locked until <t:{int(box.unlock_dt.timestamp())}:d>!",
                               mention_author=False)
                return

            boxes = [box]

        embed = discord.Embed()
        embed.title = "Open Boxes"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        boxes_dict = {}
        for box in boxes:
            boxes_dict[box] = boxes_dict.get(box, 0) + 1

        box_sets = [[box] * qty for box, qty in boxes_dict.items()]

        for box_set in box_sets:
            opened_box = box_set[0]
            for i in range(0, len(box_set), 10):
                result = member.inventory.open_boxes([(box, False) for box in box_set[i:i+10]])

                embed.add_field(
                    name=f"Opened {len(result)}x {str(opened_box)}",
                    value="\n".join(
                        [f"{str(item)}{' :sparkles:' if new_item else ''}" for item, new_item in result]
                    )
                )

        locked_lootboxes = len(member.inventory.locked_lootboxes)

        if locked_lootboxes > 0:
            embed.add_field(
                name="Locked Lootboxes",
                value=f"You have *{locked_lootboxes}* locked lootboxes!"
            )

        embeds = Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed)

        member.write_data()

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
            if Item.currentEventBox is not None:
                lootpool = Lootpool.get("HourlyEventClaim")
            else:
                lootpool = Lootpool.get("HourlyClaim")

            lootbox = lootpool.roll()

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

            lootpool = Lootpool.get("DailyClaim")
            lootbox = lootpool.roll()

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

            lootpool = Lootpool.get("WeeklyClaim")
            lootbox = lootpool.roll()

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
