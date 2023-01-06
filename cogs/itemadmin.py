import discord
from discord.ext import commands

from SharkBot import Member, Item, Errors, IDs


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
        items = [Item.get(itemid) for itemid in itemids]

        members = Member.members.values()
        for member in members:
            for item in items:
                member.inventory.add(item)
        await ctx.send(f"Granted {[item.name for item in items]} each to {len(members)} members.")

        for member in members:
            member.write_data()


async def setup(bot):
    await bot.add_cog(ItemAdmin(bot))
    print("ItemAdmin Cog loaded")


async def teardown(bot):
    print("ItemAdmin Cog unloaded")
    await bot.remove_cog(ItemAdmin(bot))
