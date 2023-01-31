import discord
from discord.ext import tasks, commands

import SharkBot


class Vault(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["v"])
    async def vault(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Vault"
        embed.description = f"`{len(member.vault):,} items`"
        embed.description += "\nItems marked with :gear: are set to auto-vault"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = member.wiki_profile_url

        for collection in SharkBot.Collection.collections:
            field_text = []
            for item in collection.items:
                if item in member.vault:
                    field_text.append(
                        f"{member.vault.count(item):,}x {item.name} *({item.id})*{member.vault.auto.flag(item)}"
                    )
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @vault.command(name="add")
    async def vault_add(self, ctx: commands.Context, item: str, num: str = "1"):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Vault Add"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        if item.lower() in ["*", "=="]:
            num = len(member.inventory)
            member.vault.add(*member.inventory.items)
            member.inventory.remove_all()
            embed.description = f"Moved {num:,} items into your Vault."
            embed.colour = discord.Colour.light_grey()
            await ctx.reply(embed=embed)
            member.write_data()
            return

        item = SharkBot.Item.get(item)

        if item not in member.inventory:
            embed.description = f"You don't have any **{member.view_of_item(item)}** in your inventory!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed)
            return

        if num.lower() in ["*", "=="]:
            num = member.inventory.count(item)
        else:
            try:
                num = int(num)
                if num < 1:
                    embed.description = f"`{num}` is not a valid number of items!"
                    embed.colour = discord.Colour.red()
                    await ctx.reply(embed=embed)
                    return
            except ValueError:
                embed.description = f"`{num}` is not a valid number!"
                embed.colour = discord.Colour.red()
                await ctx.reply(embed=embed)
                return

        if num > member.inventory.count(item):
            embed.description = f"You only have {member.inventory.count(item):,}x **{item}** in your inventory!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed)
            return

        for i in range(0, num):
            member.inventory.remove(item)
            member.vault.add(item)


        embed.description = f"Moved {num:,}x **{item}** into your Vault!"
        embed.colour = discord.Colour.light_grey()
        await ctx.reply(embed=embed)
        member.write_data()

    @vault.command(name="remove")
    async def vault_remove(self, ctx: commands.Context, item: str, num: str = "1"):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Vault Remove"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        if item.lower() in ["*", "=="]:
            num = len(member.vault)
            member.inventory.add_items(member.vault.items, ignore_vault=True)
            member.vault.remove_all()
            embed.description = f"Moved {num:,} items into your Inventory"
            embed.colour = discord.Colour.light_grey()
            await ctx.reply(embed=embed)
            member.write_data()
            return

        item = SharkBot.Item.get(item)

        if item not in member.vault:
            embed.description = f"You don't have any **{member.view_of_item(item)}** in your Vault!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed)
            return

        if num.lower() in ["*", "=="]:
            num = member.vault.count(item)
        else:
            try:
                num = int(num)
                if num < 1:
                    embed.description = f"`{num}` is not a valid number of items!"
                    embed.colour = discord.Colour.red()
                    await ctx.reply(embed=embed)
                    return
            except ValueError:
                embed.description = f"`{num}` is not a valid number!"
                embed.colour = discord.Colour.red()
                await ctx.reply(embed=embed)
                return

        if num > member.vault.count(item):
            embed.description = f"You only have {member.inventory.count(item):,}x **{str(item)}** in your Vault!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed)
            return

        for i in range(0, num):
            member.inventory.add(item, ignore_vault=True)
            member.vault.remove(item)

        embed.description = f"Moved {num:,}x **{str(item)}** into your Inventory!"
        embed.colour = discord.Colour.light_grey()
        await ctx.reply(embed=embed)
        member.write_data()

    @vault.group(invoke_without_command=True, aliases=["a"])
    async def auto(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Vault Auto"
        embed.description = f"{len(member.vault.auto):,} items set to auto-vault"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = member.wiki_profile_url

        for collection in SharkBot.Collection.collections:
            field_text = []
            for item in collection.items:
                if item in member.vault.auto:
                    item = member.view_of_item(item)
                    field_text.append(
                        f"{item.name} *({item.id})*"
                    )
            if len(field_text) == len(collection):
                field_text = ["All items in this Collection"]
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @auto.command(name="add")
    async def auto_add(self, ctx: commands.Context, item: str):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"Vault Auto Add"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_author(name=ctx.author.display_name)

        if item.lower() in ["*", "=="]:
            member.vault.auto.add(*SharkBot.Item.items)
            embed.description = f"Set **all items** to auto-vault"
            embed.colour = discord.Colour.light_grey()
        else:
            try:
                collection = SharkBot.Collection.get(item)
                member.vault.auto.add(*collection.items)
                embed.description = f"Set all items in **{str(collection)}** to auto-vault"
            except SharkBot.Errors.CollectionNotFoundError:
                item = SharkBot.Item.get(item)
                if item in member.vault.auto:
                    embed.description = f"{member.view_of_item(item)} is already set to auto-vault"
                    embed.colour = discord.Colour.red()
                else:
                    member.vault.auto.add(item)
                    embed.description = f"Set **{member.view_of_item(item)}** to auto-vault"
                    embed.colour = discord.Colour.light_grey()

        await ctx.reply(embed=embed)
        member.write_data()

    @auto.command(name="remove")
    async def auto_remove(self, ctx: commands.Context, item: str):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"Vault Auto Remove"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_author(name=ctx.author.display_name)

        if item.lower() in ["*", "all"]:
            member.vault.auto.clear()
            embed.description = "Cleared auto-vault list"
            embed.colour = discord.Colour.light_grey()
        else:
            try:
                collection = SharkBot.Collection.get(item)
                member.vault.auto.remove_collection(collection)
                embed.description = f"Removed all items in **{str(collection)}** from auto-vault"
            except SharkBot.Errors.CollectionNotFoundError:
                item = SharkBot.Item.get(item)
                try:
                    member.vault.auto.remove(item)
                    embed.description = f"Removed **{member.view_of_item(item)}** from auto-vault"
                    embed.colour = discord.Colour.light_grey()
                except SharkBot.Errors.ItemNotInVaultError:
                    embed.description = f"{member.view_of_item(item)} is already not set to auto-vault"
                    embed.colour = discord.Colour.red()

        await ctx.reply(embed=embed)
        member.write_data()

    @auto.command(name="run")
    async def auto_run(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"Vault Auto Run"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_author(name=ctx.author.display_name)
        embed.colour = discord.Colour.light_grey()

        items = [item for item in member.inventory.items if item in member.vault.auto]
        for item in items:
            member.inventory.remove(item)
            member.vault.add(item)

        embed.description = f"Auto-vaulted {len(items):,} items"

        await ctx.reply(embed=embed)
        member.write_data()




async def setup(bot):
    await bot.add_cog(Vault(bot))
    print("Vault Cog loaded")


async def teardown(bot):
    print("Vault Cog unloaded")
    await bot.remove_cog(Vault(bot))
