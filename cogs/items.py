import discord
from discord.ext import commands

import SharkBot

def format_difference(n: int) -> str:
    if n < 0:
        return str(n)
    else:
        return f"+{n}"

import logging

cog_logger = logging.getLogger("cog")

class Items(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(aliases=["search"])
    async def item(self, ctx: commands.Context, *, search: str) -> None:
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        item = SharkBot.Item.search(search)
        await ctx.reply(embed=member.view_of_item(item).embed, mention_author=False)

    @item.autocomplete("search")
    async def item_autocomplete(self, interaction: discord.Interaction, current: str):
        return await SharkBot.Autocomplete.member_discovered_item(interaction, current)

    @commands.hybrid_command(aliases=["i", "inv"])
    async def inventory(self, ctx: commands.Context) -> None:
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        member.inventory.sort()

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Inventory"
        embed.description = f"Wallet Balance: **${member.balance:,}**"
        embed.description += f"\nBank Balance: **${member.bank_balance:,}**"
        embed.description += f"\nLevel: `{member.xp.level} | {member.xp.xp:,} xp`"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = member.wiki_profile_url

        for collection in SharkBot.Collection.collections:
            field_text = []
            for item in collection.items:
                if item in member.inventory:
                    field_text.append(
                        f"{member.inventory.count(item):,}x {item.name} *({item.id})*"
                    )
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embed.add_field(
            name=":gear: Vault",
            value=f"You have {len(member.vault):,} items in your `$vault`"
        )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command()
    async def sell(self, ctx: commands.Context, *, search: str) -> None:
        search = search.upper()

        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        if search in ["ALL", "*"]:
            items = member.inventory.sellable_items
            if len(items) == 0:
                await ctx.reply("It looks like you don't have any items to sell!", mention_author=False)
                return
        elif search in ["DUPES", "D"]:
            items = [item for item in member.inventory.get_duplicates()]
            if len(items) == 0:
                await ctx.reply("It looks like you don't have any dupes! Nice!", mention_author=False)
                return
        else:
            item = SharkBot.Item.search(search)
            if not item.sellable:
                await ctx.reply(f"You can't sell **{member.view_of_item(item)}**!", mention_author=False)
                return
            if item not in member.inventory:
                await ctx.reply(f"It looks like you don't have **{member.view_of_item(item)}** to sell!", mention_author=False)
                return
            else:
                items = [item]

        sold_value = 0
        for item in items:
            try:
                member.inventory.remove(item)
                sold_value += item.value
            except SharkBot.Errors.ItemNotInInventoryError:
                items.remove(item)

        member.balance += sold_value
        await ctx.reply(
            f"Sold `{len(items):,} items` for **${sold_value:,}**. Your new balance is **${member.balance:,}**.",
            mention_author=False
        )

    @commands.command(aliases=["c", "col"])
    async def collection(self, ctx: commands.Context, *args: str) -> None:
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        if len(args) == 0:  # Collections Overview

            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Collection"
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            embed.colour = discord.Colour.blurple()

            embed.description = f"{len(member.collection):,}/{len(SharkBot.Item.items):,} items discovered"

            for collection in SharkBot.Collection.collections:
                discovered_items = len([item for item in collection.items if member.collection.contains(item)])

                embed.add_field(name=f"{collection}",
                                value=f"{discovered_items:,}/{len(collection):,} items discovered",
                                inline=False)

            await ctx.reply(embed=embed, mention_author=False)
            return

        elif args[0] in ["full", "*", "all"]:  # Full Collections Format
            collections_to_show = list(SharkBot.Collection.collections)

        else:  # Specific Collections Format

            collections_to_show = []
            for collection_name in args:
                collection = SharkBot.Collection.get(collection_name)
                if collection not in collections_to_show:
                    collections_to_show.append(collection)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Collection"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.colour = collections_to_show[-1].colour

        embed.description = f"{len(member.collection):,}/{len(SharkBot.Item.items):,} items discovered"

        for collection in collections_to_show:
            field_text = []
            for item in collection.items:
                if member.collection.contains(item):
                    field_text.append(f"{item.name} *({item.id})*")
                else:
                    field_text.append(f"??? *({item.id})*")
            embed.add_field(
                name=str(collection),
                value="\n".join(field_text),
                inline=False
            )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command()
    async def compare_collections(self, ctx: commands.Context, target: discord.Member, show_full: bool = False):
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        target_member = SharkBot.Member.get(target.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name} vs. {target.display_name}"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.colour = discord.Colour.blurple()

        difference = len(member.collection) - len(target_member.collection)

        embed.description = f"{len(member.collection):,} Items vs {len(target_member.collection):,} Items ({format_difference(difference)})"

        for collection in SharkBot.Collection.collections:
            discovered_items = len([item for item in collection.items if member.collection.contains(item)])
            target_discovered_items = len([item for item in collection.items if target_member.collection.contains(item)])

            difference = discovered_items - target_discovered_items

            if difference == 0 and not show_full:
                continue

            embed.add_field(name=f"{collection} ({format_difference(difference)})",
                            value=f"{discovered_items:,}/{len(collection):,} vs {target_discovered_items:,}/{len(collection):,} items discovered",
                            inline=False)

        await ctx.reply(embed=embed, mention_author=False)
        return

    @commands.command(aliases=["gift"])
    async def give(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)
        target_member = SharkBot.Member.get(target.id)
        try:
            item = SharkBot.Item.search(search)
        except SharkBot.Errors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return

        try:
            member.inventory.remove(item)
            response = target_member.inventory.add(item)
            await ctx.reply(f"You gave **{str(response)}** to *{target.display_name}*",
                            mention_author=False)
        except SharkBot.Errors.ItemNotInInventoryError:
            await ctx.reply(
                f"It looks like you don't have **{member.view_of_item(item)}** :pensive:",
                mention_author=False)

        target_member.write_data()


async def setup(bot):
    await bot.add_cog(Items(bot))
    print("Items Cog Loaded")
    cog_logger.info("Items Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Items(bot))
    print("Items Cog Unloaded")
    cog_logger.info("Items Cog Unloaded")