import discord
from discord.ext import commands

import SharkBot


import logging

cog_logger = logging.getLogger("cog")

class Test(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group()
    @SharkBot.Checks.is_mod()
    async def test(self, ctx: commands.Context):
        await ctx.send("Testing Commands")

    @test.command()
    async def fetch_users(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.title = "Fetch Users Test"
        embed_text = []
        embed.description = f"```Working on it...```"
        message = await ctx.send(embed=embed)
        num = len(SharkBot.Member.members)

        for i, member in enumerate(SharkBot.Member.members):
            embed_text.append(f"{member.id}... ")
            await member.fetch_discord_user(self.bot)
            user = member.discord_user
            if user is None:
                embed_text[-1] += "Failure."
            else:
                embed_text[-1] = f"{user.display_name}#{user.discriminator}... Success."
            embed.description = f"```Working on it... ({i+1}/{num})\n\n" + "\n".join(embed_text) + "```"
            await message.edit(embed=embed)
            member.write_data(upload=False)

        embed.description = f"```Done.\n\n" + "\n".join(embed_text) + "```"
        await message.edit(embed=embed)



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
    print("Test Cog Loaded")
    cog_logger.info("Test Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Test(bot))
    print("Test Cog Unloaded")
    cog_logger.info("Test Cog Unloaded")