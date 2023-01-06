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

class ItemNotInVaultError(SharkError):
    pass
