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
        embed.description = f"`{len(member.vault)} items`"
        embed.description += "\nItems marked with :gear: are set to auto-vault"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = member.wiki_profile_url

        for collection in SharkBot.Collection.collections:
            field_text = []
            for item in collection.items:
                if item in member.vault:
                    field_text.append(
                        f"{member.vault.count(item)}x {item.name} *({item.id})*{member.vault.auto.flag(item)}"
                    )
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @vault.command()
    async def add(self, ctx: commands.Context, item: str, num: str = "1"):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = "Vault Add"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        if item == "*":
            num = len(member.inventory)
            member.vault.add(*member.inventory.items)
            member.inventory.remove_all()
            embed.description = f"Moved {num} items into your Vault."
            embed.colour = discord.Colour.light_grey()
            await ctx.reply(embed=embed)
            member.write_data()
            return

        item = SharkBot.Item.get(item)

        if item not in member.inventory:
            embed.description = f"You don't have any **{str(item)}** in your inventory!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed)
            return

        if num == "*":
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
            embed.description = f"You only have {member.inventory.count(item)}x **{str(item)}** in your inventory!"
            embed.colour = discord.Colour.red()
            await ctx.reply(embed=embed)
            return

        for i in range(0, num):
            member.inventory.remove(item)
            member.vault.add(item)


        embed.description = f"Moved {num}x **{str(item)}** into your Vault!"
        embed.colour = discord.Colour.light_grey()
        await ctx.reply(embed=embed)
        member.write_data()

    @vault.group(invoke_without_command=True, aliases=["a"])
    async def auto(self, ctx: commands.Context):
        member = SharkBot.Member.get(ctx.author.id)

        embed = discord.Embed()
        embed.title = f"{ctx.author.display_name}'s Vault Auto"
        embed.description = f"{len(member.vault.auto)} items set to auto-vault"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = member.wiki_profile_url

        for collection in SharkBot.Collection.collections:
            field_text = []
            for item in collection.items:
                if item in member.vault.auto:
                    field_text.append(
                        f"{item.name} *({item.id})*"
                    )
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @auto.command()
    async def add(self, ctx: commands.Context, item: str):
        member = SharkBot.Member.get(ctx.author.id)
        item = SharkBot.Item.get(item)

        embed = discord.Embed()
        embed.title = f"Vault Auto Add"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_author(name=ctx.author.display_name)

        if item in member.vault.auto:
            embed.description = f"{str(item)} is already set to auto-vault"
            embed.colour = discord.Colour.red()
        else:
            member.vault.auto.add(item)
            embed.description = f"Set **{str(item)}** to auto-vault"
            embed.colour = discord.Colour.light_grey()

        await ctx.reply(embed=embed)
        member.write_data()



async def setup(bot):
    await bot.add_cog(Vault(bot))
    print("Vault Cog loaded")


async def teardown(bot):
    print("Vault Cog unloaded")
    await bot.remove_cog(Vault(bot))
