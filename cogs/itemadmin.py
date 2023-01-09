import discord
from discord.ext import commands

from SharkBot import Member, Item, Errors, IDs, Utils


class ItemAdmin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def add_item(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        target_member = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        response = target_member.inventory.add(item)
        await ctx.reply(f"Added **{str(response)}** to *{target.display_name}*'s inventory.", mention_author=False)
        target_member.write_data()

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def remove_item(self, ctx: commands.Context, target: discord.Member, *, search: str) -> None:
        target_member = Member.get(target.id)
        try:
            item = Item.search(search)
        except Errors.ItemNotFoundError:
            await ctx.reply("Sorry, I couldn't find that item!", mention_author=False)
            return
        try:
            target_member.inventory.remove(item)
        except Errors.ItemNotInInventoryError:
            await ctx.reply(f"Couldn't find item in *{target.display_name}*'s inventory", mention_author=False)
            return
        await ctx.reply(f"Removed **{item.name}** from *{target.display_name}*'s inventory.", mention_author=False)
        target_member.write_data()

    @commands.command()
    @commands.has_role(IDs.roles["Mod"])
    async def grant_all(self, ctx: commands.Context, *itemids: str) -> None:
        items: list[Item.Item] = [Item.get(itemid) for itemid in itemids]
        item_types: set[Item.Item] = set(items)

        members = Member.members
        for member in members:
            member.inventory.add_items(items)

        embed = discord.Embed()
        embed.title = "Grant All"
        embed.description = f"Granted `{len(items)} Items` to each of `{len(members)} Members`."
        embed.add_field(
            name="Items Granted",
            value="\n".join(f"{items.count(item)}x **{item}**" for item in item_types),
            inline=False
        )

        for e in Utils.split_embeds(embed):
            await ctx.reply(embed=e, mention_author=False)

        for member in members:
            member.write_data()


async def setup(bot):
    await bot.add_cog(ItemAdmin(bot))
    print("ItemAdmin Cog loaded")


async def teardown(bot):
    print("ItemAdmin Cog unloaded")
    await bot.remove_cog(ItemAdmin(bot))
