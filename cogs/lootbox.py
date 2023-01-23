import discord
from discord.ext import commands

from SharkBot import Item, Member, Views, Utils, Lootpool, EventCalendar


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
            if box not in member.inventory:
                await ctx.send(f"I'm afraid you don't have any **{box}**!", mention_author=False)
                return
            if not box.unlocked:
                await ctx.send(f"That lootbox is locked until <t:{int(box.unlock_dt.timestamp())}:d>!",
                               mention_author=False)
                return

            boxes = [box]

        embed = discord.Embed()
        embed.title = "Open Boxes"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        boxes_dict = {}
        for box in boxes:
            boxes_dict[box] = boxes_dict.get(box, 0) + 1

        box_sets = [[box] * qty for box, qty in boxes_dict.items()]

        for box_set in box_sets:
            opened_box = box_set[0]
            for i in range(0, len(box_set), 10):
                results = member.inventory.open_boxes([(box, False) for box in box_set[i:i+10]])

                embed.add_field(
                    name=f"Opened {len(results)}x {str(opened_box)}",
                    value="\n".join(result.item_printout for result in results)
                )

        if len(member.inventory.locked_lootboxes) > 0:
            locked_lootboxes = set(member.inventory.locked_lootboxes)
            embed.add_field(
                name="Locked Lootboxes",
                value="\n".join(
                    [f"{member.inventory.count(item)}x {str(item)} *({item.id})*" for item in locked_lootboxes]
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
        embed.description = "Free shit!"

        claimed_boxes = []

        for cooldown in member.cooldowns.active_claims:
            cooldown_name = cooldown.name.title()
            if cooldown.expired:  # Hourly Claim
                cooldown.reset()

                lootpool = Lootpool.get(f"{cooldown_name}Claim")
                if lootpool.id == "EventClaim":
                    lootpool = Lootpool.get(f"EventClaimLNY")
                lootbox = lootpool.roll()

                claimed_boxes.append(lootbox)
                response = member.inventory.add(lootbox)
                embed.add_field(name=cooldown_name,
                                value=f"Success! You claimed a **{str(response)}**!",
                                inline=False)
            else:
                embed.add_field(name=cooldown_name,
                                value=f"You still have {cooldown.time_remaining_string} left!",
                                inline=False)

        event_calendar = EventCalendar.get_current()
        if event_calendar is not None:
            index = event_calendar.get_current_index()
            if event_calendar.member_can_claim(member, index):
                rewards = event_calendar.get_rewards(index)
                claimed_boxes.extend(rewards)
                responses = member.inventory.add_items(rewards)
                output = []
                for item in set(rewards):
                    num = rewards.count(item)
                    response = [r for r in responses if r.item == item][0]
                    output.append(f"{num}x **{response}**")
                embed.add_field(
                    name=event_calendar.name,
                    value="\n".join(output),
                    inline=False
                )
                event_calendar.mark_member_claimed(member, index)
            else:
                embed.set_footer(text=f"{event_calendar.name} reward already claimed today!")

        await ctx.reply(embed=embed, mention_author=False)

        if claimed_boxes:
            await member.missions.log_action("claim", ctx)
            member.stats.claims += 1
            member.stats.boxes.claimed += len(claimed_boxes)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.write_data()


async def setup(bot):
    await bot.add_cog(Lootbox(bot))
    print("Lootbox Cog loaded")


async def teardown(bot):
    print("Lootbox Cog unloaded")
    await bot.remove_cog(Lootbox(bot))
