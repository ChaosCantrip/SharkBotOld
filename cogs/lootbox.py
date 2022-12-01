import discord
from discord.ext import commands, tasks

import random

from SharkBot import Item, Member, Views, Utils, Lootpool, Listing


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

        if len(member.inventory.locked_lootboxes) > 0:
            locked_lootboxes = set(member.inventory.locked_lootboxes)
            embed.add_field(
                name="Locked Lootboxes",
                value="\n".join(
                    [f"{member.inventory.count(item)}x {item.name} *({item.id})*" for item in locked_lootboxes]
                ),
                inline=False
            )

        embeds = Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

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

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.write_data()

    @commands.command()
    async def buy_cycle(self, ctx: commands.Context, *, search: str):
        member = Member.get(ctx.author.id)
        box = Item.get(search)

        if box.type == "Item":
            await ctx.reply(f"**{str(box)}** isn't a lootbox!")
            return
        if not box.unlocked:
            await ctx.reply(f"**{str(box)}** is locked until <t:{int(box.unlock_dt.timestamp())}:d>!")
            return
        if box not in Listing.availableItems:
            await ctx.reply(f"**{str(box)}** isn't available in the shop!")
            return

        listing = discord.utils.get(Listing.listings, item=box)

        if member.balance < listing.price:
            await ctx.reply(f"I'm afraid you don't have enough to buy **{str(box)}** (${listing.price})")
            return

        embeds = []

        i = 0
        new_items = 0
        boxes_cycled = 0
        while member.balance >= listing.price:
            i += 1
            embeds.append(discord.Embed())
            embeds[-1].set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar.url
            )
            embeds[-1].title = f"Buy Cycling {str(box)} - Cycle {i}"

            boxes: list[Item.Lootbox] = [box] * (member.balance // listing.price)
            member.balance -= listing.price * len(boxes)
            member.inventory.add_items(boxes)
            embeds[-1].description = f"Bought {len(boxes)}x **{str(box)}**"

            items = []
            for box in boxes:
                boxes_cycled += 1
                item = box.roll()
                items.append((item, not member.collection.contains(item)))
                member.inventory.remove(box)
                member.inventory.add(item)

            field_lines = []
            for item, new in items:
                if new:
                    new_items += 1
                    field_lines.append(f"{str(item)} :sparkles:")
                else:
                    field_lines.append(f"{str(item)}")

            embeds[-1].add_field(
                name="Opened Items",
                value="\n".join(field_lines),
                inline=False
            )

            sold_sum = 0
            for item in [tup[0] for tup in items]:
                sold_sum += item.value
                member.inventory.remove(item)

            member.balance += sold_sum

            embeds[-1].add_field(
                name="Selling Items",
                value=f"Sold {len(items)} items for *${sold_sum}*. Your new balance is *${member.balance}.*"
            )

        embeds.append(discord.Embed())
        embeds[-1].set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar.url
        )
        embeds[-1].title = "Buy Cycle Finished"
        embeds[-1].description = f"You cycled through *{boxes_cycled}* boxes and discovered **{new_items}** new items!"

        final_embeds = []
        for embed in embeds:
            final_embeds += Utils.split_embeds(embed)

        for embed in final_embeds:
            await ctx.reply(embed=embed, mention_author=False)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.write_data()


async def setup(bot):
    await bot.add_cog(Lootbox(bot))
    print("Lootbox Cog loaded")


async def teardown(bot):
    print("Lootbox Cog unloaded")
    await bot.remove_cog(Lootbox(bot))
