import discord
from discord.ext import commands

from SharkBot import Member, Errors, Item, Collection, Utils


class Items(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(aliases=["search"])
    async def item(self, ctx: commands.Context, *, search: str) -> None:
        member = Member.get(ctx.author.id)
        item = Item.search(search)
        if member.collection.contains(item):
            await ctx.reply(embed=item.embed, mention_author=False)
        else:
            fake_item = Item.FakeItem(item)
            await ctx.reply(embed=fake_item.embed, mention_author=False)

    @commands.hybrid_command(aliases=["i", "inv"])
    async def inventory(self, ctx: commands.Context) -> None:
        member = Member.get(ctx.author.id)
        member.inventory.sort()

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Inventory"
        embed.description = f"Balance: `${member.balance}`\nLevel: `{member.xp.level} | {member.xp.xp} xp`"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        for collection in Collection.collections:
            field_text = []
            for item in collection.items:
                if member.inventory.contains(item):
                    field_text.append(
                        f"{member.inventory.count(item)}x {item.name} *({item.id})*"
                    )
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embeds = Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

        member.write_data()

    @commands.hybrid_command()
    async def sell(self, ctx: commands.Context, *, search: str) -> None:
        search = search.upper()

        member = Member.get(ctx.author.id)

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
            item = Item.search(search)
            if not item.sellable:
                await ctx.reply(f"You can't sell **{item}**!", mention_author=False)
                return
            if not member.inventory.contains(item):
                await ctx.reply(f"It looks like you don't have **{item}** to sell!", mention_author=False)
                return
            else:
                items = [item]

        sold_value = 0
        for item in items:
            try:
                member.inventory.remove(item)
                sold_value += item.value
            except Errors.ItemNotInInventoryError:
                items.remove(item)

        member.balance += sold_value
        await ctx.reply(
            f"Sold `{len(items)} items` for **${sold_value}**. Your new balance is **${member.balance}**.",
            mention_author=False
        )

        member.write_data()

    @commands.command(aliases=["c", "col"])
    async def collection(self, ctx: commands.Context, *args: str) -> None:
        member = Member.get(ctx.author.id)

        if len(args) == 0:  # Collections Overview

            embed = discord.Embed()
            embed.title = f"{ctx.author.display_name}'s Collection"
            embed.set_thumbnail(url=ctx.author.display_avatar.url)

            embed.description = f"{len(member.collection)}/{len(Item.items)} items discovered"

            for collection in Collection.collections:
                discovered_items = len([item for item in collection.items if member.collection.contains(item)])

                embed.add_field(name=f"{collection}",
                                value=f"{discovered_items}/{len(collection)} items discovered",
                                inline=False)

            await ctx.reply(embed=embed, mention_author=False)
            return

        elif args[0] in ["full", "*", "all"]:  # Full Collections Format
            collections_to_show = list(Collection.collections)

        else:  # Specific Collections Format

            collections_to_show = []
            for collection_name in args:
                collection = Collection.get(collection_name)
                if collection not in collections_to_show:
                    collections_to_show.append(collection)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Collection"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        embed.description = f"{len(member.collection)}/{len(Item.items)} items discovered"

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

        embeds = Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["gift"])
    async def give(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        member = Member.get(ctx.author.id)
        target_member = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("I'm afraid I couldn't find that item!", mention_author=False)
            return

        try:
            member.inventory.remove(item)
            target_member.inventory.add(item)
            await ctx.reply(f"You gave **{str(item)}** to *{target.display_name}*",
                            mention_author=False)
        except Errors.ItemNotInInventoryError:
            await ctx.reply(
                f"It looks like you don't have **{str(item)}** :pensive:",
                mention_author=False)
        member.write_data()

        target_member.write_data()


async def setup(bot):
    await bot.add_cog(Items(bot))
    print("Items Cog loaded")


async def teardown(bot):
    print("Items Cog unloaded")
    await bot.remove_cog(Items(bot))
