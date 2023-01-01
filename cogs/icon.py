from typing import Optional

import discord
from discord.ext import commands

import SharkBot


class Icon(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
        if guild.id != SharkBot.IDs.icon_source_guild:
            return

        print("\nIcons Change Detected... ", end="")
        if not SharkBot.Icon.check(guild=guild):
            print("New Icons Found.")
            print("Fetching new Icons... ", end="")
            SharkBot.Icon.extract(guild=guild)
            print("Done.\n")
            dev = await self.bot.fetch_user(SharkBot.IDs.dev)
            await dev.send("Icon changes imported.")
        else:
            print("No New Icons Found.\n")

    @commands.group(invoke_without_command=True)
    async def icon(self, ctx: commands.Context, icon_name: str):
        if icon_name.startswith(":") and icon_name.endswith(":"):
            icon_name = icon_name[1:-1]
        _icon = SharkBot.Icon.get(icon_name)

        if _icon == SharkBot.Icon.PLACEHOLDER:
            await ctx.reply(f"I'm afraid `{icon_name}` is not a SharkBot Icon.")
            return

        _icon_id = _icon.split(":")[-1][:-1]

        embed = discord.Embed()
        embed.title = f"SharkBot Icon - `{icon_name}`"
        embed.add_field(
            name="Icon ID",
            value=f"`{_icon}`"
        )
        embed.set_thumbnail(
            url=f"https://cdn.discordapp.com/emojis/{_icon_id}.png"
        )

        await ctx.reply(embed=embed, mention_author=False)

    @icon.command()
    @commands.has_role(SharkBot.IDs.roles["Mod"])
    async def list(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.title = "Icon List"
        for name, icon in SharkBot.Icon.icon_dict().items():
            embed.add_field(
                name=f"{icon} {name}",
                value=f"`{icon}`",
                inline=False
            )

        for e in SharkBot.Utils.split_embeds(embed):
            await ctx.send(embed=e)

    @icon.command()
    @commands.has_role(SharkBot.IDs.roles["Mod"])
    async def refresh(self, ctx: commands.Context, guild: Optional[discord.Guild]):
        if guild is None:
            guild = self.bot.get_guild(SharkBot.IDs.icon_source_guild)
            if guild is None:
                guild = await self.bot.fetch_guild(SharkBot.IDs.icon_source_guild)

        embed = discord.Embed()
        embed.title = "Icon Refresh"
        embed.add_field(
            name="Before Refresh",
            value=f"{len(SharkBot.Icon.icon_dict())} Icons Saved",
            inline=False
        )

        SharkBot.Icon.extract(guild=guild)

        embed.add_field(
            name="After Refresh",
            value=f"{len(SharkBot.Icon.icon_dict())} Icons Saved",
            inline=False
        )

        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot):
    await bot.add_cog(Icon(bot))
    print("Icon Cog loaded")


async def teardown(bot):
    print("Icon Cog unloaded")
    await bot.remove_cog(Icon(bot))
