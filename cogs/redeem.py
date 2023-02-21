import logging

import discord
from discord.ext import commands

import SharkBot

cog_logger = logging.getLogger("cog")

class Redeem(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def redeem(self, ctx: commands.Context, search: str):
        embed = discord.Embed()
        embed.title = "Redeem"
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        code = SharkBot.Code.get(search)
        member = SharkBot.Member.get(ctx.author.id, discord_user=ctx.author)

        if code.code in member.used_codes:
            embed.colour = discord.Colour.red()
            embed.description = f"You have already redeemed that code!"
            await ctx.send(embed=embed)
            return

        if code.expired:
            embed.colour = discord.Colour.red()
            embed.description = f"Sorry, that code has expired!"
            await ctx.send(embed=embed)
            return

        money_reward = code.money_reward
        item_rewards = code.item_rewards
        xp_reward = code.xp_reward

        embed.colour = discord.Colour.green()
        embed.description = f"You redeemed a code!"
        if money_reward is not None:
            member.balance += money_reward
            embed.add_field(
                name="Shark Coins Reward",
                value=f"**${money_reward:,}**",
                inline=False
            )
        if item_rewards is not None:
            responses = member.inventory.add_items(item_rewards)
            responses_dict = {}
            for response in responses:
                if responses_dict.get(response.item) is None:
                    responses_dict[response.item] = response
            num_dict = {}
            for item, response in responses_dict.items():
                num_dict[response] = item_rewards.count(item)
            embed.add_field(
                name="Item Rewards",
                value="\n".join(f"{num}x **{str(response)}**" for response, num in num_dict.items()),
                inline=False
            )
        if xp_reward is not None:
            embed.add_field(
                name="XP Reward",
                value=f"`{xp_reward:,} xp`",
                inline=False
            )

        for e in SharkBot.Utils.split_embeds(embed):
            await ctx.channel.send(embed=e)

        if xp_reward is not None:
            await member.xp.add(xp_reward, ctx)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.used_codes += [code.code]

        if ctx.guild is not None:
            await ctx.message.delete()
            embed.set_footer(
                text="This is a public channel, so I removed your message. Use $redeem in DMs to me next time!"
            )

        dev = await self.bot.fetch_user(SharkBot.IDs.dev)
        await dev.send(f"*{ctx.author.display_name}* redeemed code `{code.code}`")

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def a_code(self, ctx: commands.Context):
        await ctx.reply("Admin Code Commands")

    @a_code.command()
    @commands.is_owner()
    async def add_code(self, ctx: commands.Context, code: str):
        code = code.upper()
        SharkBot.Code.add_code(code)
        await ctx.reply(f"Created code `{code}`.")

    @a_code.command()
    @commands.is_owner()
    async def del_code(self, ctx: commands.Context, code: str):
        code = code.upper()
        SharkBot.Code.remove_code(code)
        await ctx.reply(f"Removed code `{code}`")

    @a_code.command()
    @commands.is_owner()
    async def add_money(self, ctx: commands.Context, search: str, amount: int):
        code = SharkBot.Code.a_get(search)
        code.add_reward(
            reward_type="money",
            reward=amount
        )
        await ctx.reply(f"Added **${amount}** to `{code.code}`")

    @a_code.command()
    @commands.is_owner()
    async def add_item(self, ctx: commands.Context, code_id: str, item_id: str, num: int = 1):
        code = SharkBot.Code.a_get(code_id)
        item = SharkBot.Item.get(item_id)
        for i in range(num):
            code.add_reward(
                reward_type="item",
                reward=item.id
            )
        await ctx.reply(f"Added {num}x **{str(item)}** to `{code.code}`")

    @a_code.command()
    @commands.is_owner()
    async def add_xp(self, ctx: commands.Context, search: str, amount: int):
        code = SharkBot.Code.a_get(search)
        code.add_reward(
            reward_type="xp",
            reward=amount
        )
        await ctx.reply(f"Added `{amount} xp` to `{code.code}`")



async def setup(bot):
    await bot.add_cog(Redeem(bot))
    print("Redeem Cog Loaded")
    cog_logger.info("Redeem Cog Loaded")


async def teardown(bot):
    await bot.remove_cog(Redeem(bot))
    print("Redeem Cog Unloaded")
    cog_logger.info("Redeem Cog Unloaded")