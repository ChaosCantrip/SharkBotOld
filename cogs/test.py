import discord
from discord.ext import commands, tasks

import SharkBot


class Test(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group()
    @commands.has_role(SharkBot.IDs.roles["Mod"])
    async def test(self, ctx: commands.Context):
        await ctx.send("Testing Commands")

    @test.command()
    async def item_names(self, ctx: commands.Context):
        longest_name = max(SharkBot.Item.items, key=lambda item: len(item.name))
        longest_text = max(SharkBot.Item.items, key=lambda item: len(str(item)))
        longest_description = max(SharkBot.Item.items, key=lambda item: len(item.description))
        longest_combined = max(SharkBot.Item.items, key=lambda item: len(str(item)) + len(item.description))

        embed = discord.Embed()
        embed.title = "Item Names"
        embed.add_field(
            name="Longest Name",
            value=f"{longest_name} | {len(longest_name.name)}",
            inline=False
        )
        embed.add_field(
            name="Longest Text",
            value=f"{longest_text} | {len(str(longest_text))}",
            inline=False
        )
        embed.add_field(
            name="Longest Description",
            value=f"{longest_description} | {len(longest_description.description)}",
            inline=False
        )
        embed.add_field(
            name="Longest Combined",
            value=f"{longest_combined} | {len(longest_combined.description) + len(str(longest_combined))}",
            inline=False
        )

        await ctx.reply(embed=embed, mention_author=False)

    @test.command()
    async def item_chunking(self, ctx: commands.Context, chunk_length: int = 15):
        embed = discord.Embed()
        embed.title = f"Item Chunking - {chunk_length}"

        for collection in SharkBot.Collection.collections:
            chunks = [collection.items[i:i+chunk_length] for i in range(0, len(collection), chunk_length)]
            embed.add_field(
                name=f"{collection}",
                value="\n".join(
                    [f"Chunk {chunks.index(chunk) + 1}: {sum([len(str(item)) for item in chunk])}" for chunk in chunks]
                ),
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Test(bot))
    print("Test Cog loaded")


async def teardown(bot):
    print("Test Cog unloaded")
    await bot.remove_cog(Test(bot))
