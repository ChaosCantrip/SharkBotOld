import discord
from discord.ext import commands


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
    pass


class RarityNotFoundError(SharkError):
    pass


class ItemNotFoundError(SharkError):

    def __init__(self, search):
        self.search = search

    async def handler(self, ctx: commands.Context) -> bool:
        embed = discord.Embed()
        embed.title = "Item Not Found"
        embed.description = f"I'm afraid I couldn't find *\"{self.search}\"*"
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
