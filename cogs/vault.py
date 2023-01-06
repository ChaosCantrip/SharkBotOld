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
        embed.description = f"{len(member.vault)} items"
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.url = member.wiki_profile_url

        for collection in SharkBot.Collection.collections:
            field_text = []
            for item in collection.items:
                if item in member.vault:
                    field_text.append(
                        f"{member.vault.count(item)}x {item.name} *({item.id})*"
                    )
            if len(field_text) > 0:
                embed.add_field(
                    name=str(collection),
                    value="\n".join(field_text)
                )

        embeds = SharkBot.Utils.split_embeds(embed)
        for embed in embeds:
            await ctx.reply(embed=embed, mention_author=False)

    @vault.command(aliases=["a"])
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


async def setup(bot):
    await bot.add_cog(Vault(bot))
    print("Vault Cog loaded")


async def teardown(bot):
    print("Vault Cog unloaded")
    await bot.remove_cog(Vault(bot))
