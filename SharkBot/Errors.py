import json

import discord
from discord.ext import commands
import SharkBot

from aiohttp import ClientResponse
from requests import Response


class SharkError(Exception):

    async def report(self, ctx: commands.Context):
        return

    async def handler(self, ctx: commands.Context) -> bool:
        return False


class MemberFileNotFoundError(SharkError):
    pass


class AccountAlreadyLinkedError(SharkError):
    pass


class AccountNotLinkedError(SharkError):
    pass


class AccountAlreadyInUseError(SharkError):
    pass


class ItemNotInInventoryError(SharkError):
    pass


class ItemNotInCollectionError(SharkError):
    pass


class CollectionNotFoundError(SharkError):

    def __init__(self, search: str):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        embed = discord.Embed()
        embed.title = "Collection Not Found"
        embed.description = f"I'm afraid I couldn't find `{self.search.title()}`"
        similar = SharkBot.Utils.get_similar_collections(self.search)
        if similar is not None:
            embed.description += f"\nDid you mean `{similar.title()}`?"
        embed.colour = discord.Colour.red()
        await ctx.reply(embed=embed, mention_author=False)

        return True


class RarityNotFoundError(SharkError):
    pass


class ItemNotFoundError(SharkError):

    def __init__(self, search: str):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        embed = discord.Embed()
        embed.title = "Item Not Found"
        embed.description = f"I'm afraid I couldn't find `{self.search.title()}`"
        similar = SharkBot.Utils.get_similar_items(self.search)
        if similar is not None:
            embed.description += f"\nDid you mean `{similar.title()}`?"
        embed.colour = discord.Colour.red()
        await ctx.reply(embed=embed, mention_author=False)

        return True


class TestError(SharkError):
    pass


class MissionNotFoundError(SharkError):
    pass


class MissionTypeNotFoundError(SharkError):
    pass


class LootpoolNotFoundError(SharkError):
    pass


class UnknownLootpoolNodeType(SharkError):
    pass


class InvalidCodeError(SharkError):

    def __init__(self, code: str):
        self.code = code

    async def handler(self, ctx: commands.Context) -> bool:
        await ctx.send(f"That is not a valid code to redeem!")

        return True


class CodeAlreadyExistsError(SharkError):

    def __init__(self, search: str):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        await ctx.send(f"Code `{self.search}` already exists")

        return True


class CodeDoesNotExistError(SharkError):

    def __init__(self, search: str):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        await ctx.send(f"Code `{self.search}` does not exist!")

        return True


class ZIPBackup:

    class BackupDoesNotExistError(SharkError):
        pass


class BankBalanceBelowZeroError(SharkError):
    pass

class BalanceBelowZeroError(SharkError):
    pass

class ItemNotInVaultError(SharkError):
    pass

class Effects:

    class InvalidEffectDataError(SharkError):
        pass

    class EffectNotActiveError(SharkError):
        pass

    class NotEnoughChargesError(SharkError):
        pass

    class EffectDoesNotHaveChargesError(SharkError):
        pass

    class InvalidSizeError(SharkError):
        pass

    class UnknownConsumableError(SharkError):
        pass


class BungieAPI:

    class TokenRefreshFailedError(SharkError):

        def __init__(self, member, response: ClientResponse, content: str):
            self.member: SharkBot.Member.Member = member
            self.response = response
            self.status = response.status
            self.reason = response.reason
            try:
                self.content: dict = json.loads(content)
            except json.JSONDecodeError:
                self.content: dict = {"response_content": content}
            if self.content.get("response", {}).get("error_description") == "SystemDisabled":
                self.status = 503
                self.reason = "System Unavailable"

        async def report(self, ctx: commands.Context):
            if self.status == 503:
                return
            dev = await ctx.bot.fetch_user(SharkBot.IDs.dev)
            embed = discord.Embed(
                title="Token Refresh Failed!",
                colour=discord.Colour.red()
            )
            embed.add_field(
                name=f"Target: `{self.member.raw_display_name} | {self.member.id}`",
                value=f"{self.status } | {self.reason}",
                inline=False
            )
            embed.add_field(
                name="Content",
                value="```" + json.dumps(self.content, indent=2) + "```",
                inline=False
            )

            for e in SharkBot.Utils.split_embeds(embed):
                await dev.send(embed=e)

        async def handler(self, ctx: commands.Context) -> bool:
            embed = discord.Embed()
            embed.title = "Something went wrong!"
            embed.colour = discord.Colour.red()
            if self.status == 503:
                embed.description = f"The Bungie API is currently disabled, please try again later."
            else:
                embed.description = f"Something went wrong while connecting to the OAuth2 endpoint, I've told <@220204098572517376> to have a look!"
            await ctx.reply(embed=embed)

            return True

    class InternalServerError(SharkError):

        def __init__(self, status: int, reason: str):
            self.status = status
            self.reason = reason

        async def handler(self, ctx: commands.Context) -> bool:
            embed = discord.Embed()
            embed.title = "Something went wrong!"
            embed.colour = discord.Colour.red()
            embed.description = f"Something's fucky with the backend, I've told <@220204098572517376> to have a look!"
            await ctx.reply(embed=embed)

            return True


    class SetupNeededError(SharkError):
        def __init__(self, member_id: int):
            self.member_id = member_id

        async def handler(self, ctx: commands.Context) -> bool:
            embed = discord.Embed()
            embed.title = "Bungie not Authorised!"
            embed.colour = discord.Colour.blurple()
            embed.description = f"You need to authorise SharkBot with Bungie to get this data! Use </bungie_auth:1079377403295563837> to get started!"
            await ctx.reply(embed=embed)

            return True


    class FollowupMessageError(SharkError):

        def __init__(self, ctx:commands.Context, cache_embed: discord.Embed, messages: list[discord.Message], e, bungie_data):
            self.ctx = ctx
            self.cache_embed = cache_embed
            self.messages = messages
            self.error: BungieAPI.InternalServerError | BungieAPI.TokenRefreshFailedError = e
            self.bungie_data: SharkBot.BungieData = bungie_data

        async def report(self, ctx: commands.Context):
            await self.error.report(ctx)

        async def handler(self, ctx: commands.Context) -> bool:
            self.cache_embed.colour = discord.Colour.red()
            self.cache_embed.set_thumbnail(
                url="https://i.ytimg.com/vi/8tPj5L19-9U/maxresdefault.jpg"
            )
            self.cache_embed.set_footer(
                text=f"{self.error.status} | {self.error.reason} | {type(self.error).__name__}"
            )
            if self.cache_embed.description is None:
                self.cache_embed.description = ""
            self.cache_embed.description = f"**Something Went Wrong while fetching your {type(self.bungie_data).__name__} Data**\n This is usually down to the Bungie API going offline, it should be back later!\n" + self.cache_embed.description
            await SharkBot.Utils.Embed.reply_with_replace(self.cache_embed, self.ctx, self.messages)
            return True

class CommandDisabledError(SharkError):
    pass

class SourceNotFoundError(SharkError):

    def __init__(self, search: str):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        embed = discord.Embed()
        embed.title = "Source Not Found!"
        embed.description = f"I'm afraid I couldn't find `{self.search}` as a choice for red border weapons!"
        embed.colour = discord.Colour.red()
        await ctx.reply(embed=embed, mention_author=False)

        return True


class LeaderboardNotFoundError(SharkError):

    def __init__(self, search: str):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        embed = discord.Embed()
        embed.title = "Leaderboard Not Found!"
        embed.description = f"I'm afraid I couldn't find `{self.search}` as a leaderboard!"
        embed.add_field(
            name="__Available Leaderboards__",
            value="\n".join(f"- `{lb.name}`" for lb in SharkBot.Leaderboard.Leaderboard.leaderboards)
        )
        embed.colour = discord.Colour.red()
        await ctx.reply(embed=embed, mention_author=False)

        return True


class ItemIsNotLootboxError(SharkError):
    pass


class ItemIsNotConsumableError(SharkError):
    pass


class CountBoxMessageExistsError(SharkError):
    pass




class Manifest:

    class ManifestNotFoundError(SharkError):
        pass

    class DefinitionTypeDoesNotExistError(SharkError):
        pass

    class DefinitionFileNotFoundError(SharkError):
        pass

    class DefinitionNotFoundError(SharkError):
        pass

    class FetchFailedError(SharkError):

        def __init__(self, target: str, response: Response | ClientResponse, content: str):
            self.target = target
            self.response = response
            self.reason = response.reason
            if isinstance(response, Response):
                self.status_code = response.status_code
            else:
                self.status_code = response.status
            try:
                self.content = json.dumps(json.loads(content), indent=2)
            except Exception as e:
                self.content = content

        async def report(self, ctx: commands.Context):
            if self.status_code == 503:
                return
            dev = await ctx.bot.fetch_user(SharkBot.IDs.dev)
            embed = discord.Embed(
                title="Fetch Failed!",
                colour=discord.Colour.red()
            )
            embed.add_field(
                name=f"Target: `{self.target}`",
                value=f"{self.status_code} | {self.reason}",
                inline=False
            )
            embed.add_field(
                name="Content",
                value=self.content,
                inline=False
            )

            for e in SharkBot.Utils.split_embeds(embed):
                await dev.send(embed=e)


        async def handler(self, ctx: commands.Context) -> bool:
            embed = discord.Embed(
                title="Fetch Failed!",
                description="Something went wrong fetching the data from Bungie! Usually this is because the Bungie API is down, I'm sure it'll be back later!",
                colour=discord.Colour.red()
            )
            if self.status_code == 503:
                embed.description = "The Bungie API is currently down for maintenance, please try again later!"
            embed.set_footer(
                text=f"{self.status_code} | {self.reason}"
            )
            await ctx.send(embed=embed)
            return True

    class HashesNotFoundError(SharkError):
        pass


    class InvalidHashesError(SharkError):
        pass