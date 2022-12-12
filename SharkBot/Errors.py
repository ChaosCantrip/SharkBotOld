import discord
from discord.ext import commands
import SharkBot


class SharkError(Exception):

    # noinspection PyUnusedLocal
    @staticmethod
    async def handler(ctx: commands.Context) -> bool:
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
    pass


class CodeAlreadyExistsError(SharkError):
    pass
