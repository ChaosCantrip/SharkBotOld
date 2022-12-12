import discord
from discord.ext import tasks, commands

import SharkBot


class Redeem(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def redeem(self, ctx: commands.Context, search: str):
        embed = discord.Embed()
        embed.title = "Redeem"
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        if ctx.guild is not None:
            await ctx.message.delete()
            embed.colour = discord.Colour.red()
            embed.description = "Don't redeem codes in public channels! Use `$redeem` in a DM to me directly!"
            await ctx.send(embed=embed)
            return

        code = SharkBot.Code.get(search)
        member = SharkBot.Member.get(ctx.author.id)

        if code.code in member.used_codes:
            embed.colour = discord.Colour.red()
            embed.description = f"You have already redeemed the code `{code.code}`!"
            await ctx.send(embed=embed)
            return

        if code.expired:
            embed.colour = discord.Colour.red()
            embed.description = f"Sorry, the code `{code.code}` has expired!"
            await ctx.send(embed=embed)
            return

        member.used_codes.append(code.code)
        money_reward = code.money_reward
        item_rewards = code.item_rewards
        xp_reward = code.xp_reward

        embed.colour = discord.Colour.green()
        embed.description = f"You redeemed the code `{code.code}`!"
        if money_reward is not None:
            member.balance += money_reward
            embed.add_field(
                name="Shark Coins Reward",
                value=f"**${money_reward}**",
                inline=False
            )
        if item_rewards is not None:
            member.inventory.add_items(item_rewards)
            embed.add_field(
                name="Item Rewards",
                value="\n".join(str(item) for item in item_rewards),
                inline=False
            )
        if xp_reward is not None:
            embed.add_field(
                name="XP Reward",
                value=f"`{xp_reward} xp`",
                inline=False
            )

        await ctx.send(embed=embed)

        if xp_reward is not None:
            await member.xp.add(xp_reward, ctx)

        if member.collection.xp_value_changed:
            await member.xp.add(member.collection.commit_xp(), ctx)

        member.write_data()

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
    async def add_money(self, ctx: commands.Context, search: str, amount: int):
        code = SharkBot.Code.a_get(search)
        code.add_reward(
            reward_type="money",
            reward=amount
        )
        await ctx.reply(f"Added **${amount}** to `{code.code}`")

    @a_code.command()
    @commands.is_owner()
    async def add_item(self, ctx: commands.Context, search: str, item_search: str):
        code = SharkBot.Code.a_get(search)
        item = SharkBot.Item.get(item_search)
        code.add_reward(
            reward_type="item",
            reward=item.id
        )
        await ctx.reply(f"Added {str(item)} to `{code.code}`")

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
    print("Redeem Cog loaded")


async def teardown(bot):
    print("Redeem Cog unloaded")
    await bot.remove_cog(Redeem(bot))
