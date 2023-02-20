import SharkBot
from discord import Interaction
from discord.app_commands import Choice

def items_to_choices(items: list[SharkBot.Item.Item]) -> list[Choice]:
    return [
        Choice(
            name=f"[{item.id}] {item.name}",
            value=item.id
        ) for item in list(set(items))[0:25]
    ]

def balance_to_choices(numbers: list[int]) -> list[Choice]:
    return [
        Choice(
            name=f"${numbers[0]} - Balance",
            value=numbers[0]
        )
    ] + [
        Choice(
            name=f"${number}",
            value=number
        ) for number in numbers[1:]
    ]

class Autocomplete:

    @staticmethod
    async def inventory_item(interaction: Interaction, current: str):
        member = SharkBot.Member.get(interaction.user.id, create=False)
        return items_to_choices(
            member.inventory.filter(lambda i: SharkBot.Utils.item_startswith(i, current.lower()))
        )

    @staticmethod
    async def member_discovered_item(interaction: Interaction, current: str):
        member = SharkBot.Member.get(interaction.user.id, create=False)
        return items_to_choices(
            [item for item in member.collection.items if SharkBot.Utils.item_startswith(item, current.lower())]
        )

    @staticmethod
    async def openable_item(interaction: Interaction, current: str):
        member = SharkBot.Member.get(interaction.user.id, create=False)
        return items_to_choices(
            [item for item in member.inventory.filter(lambda i: i.openable) if SharkBot.Utils.item_startswith(item, current.lower())]
        )

    @staticmethod
    async def member_balance(interaction: Interaction, current: str) -> list[Choice]:
        member = SharkBot.Member.get(interaction.user.id, create=False)
        try:
            current = int(current)
        except ValueError:
            return balance_to_choices([member.balance, 100, 10])
        if current >= member.balance:
            return balance_to_choices([member.balance, 100, 10])
        else:
            diff = (member.balance - current) // 5
            return balance_to_choices([member.balance, 100, 10] + list(range(current, member.balance, diff)))
