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
        await ctx.reply(
            f"I'm afraid I couldn't find `{self.search}`. Make sure you're typing it correctly!",
            mention_author=False
        )
        return True


class TestError(SharkError):
    pass


class MissionNotFoundError(SharkError):
    pass


class MissionTypeNotFoundError(SharkError):
    pass
