import SharkBot
from discord import Interaction
from discord.app_commands import Choice

SEAL_HASHES: dict[str, str] = {
    seal_name: seal_hash
    for seal_name, seal_hash in SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealHashes.json").items()
}

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
            name=f"${number}",
            value=number
        ) for number in numbers
    ]

class Autocomplete:

    @staticmethod
    async def inventory_item(interaction: Interaction, current: str):
        member = SharkBot.Member.get(interaction.user.id, create=False)
        return items_to_choices(
            member.inventory.filter(lambda i: SharkBot.Utils.item_contains(i, current.lower()))
        )

    @staticmethod
    async def member_discovered_item(interaction: Interaction, current: str):
        member = SharkBot.Member.get(interaction.user.id, create=False)
        return items_to_choices(
            [item for item in member.collection.items if SharkBot.Utils.item_contains(item, current.lower())]
        )

    @staticmethod
    async def openable_item(interaction: Interaction, current: str):
        member = SharkBot.Member.get(interaction.user.id, create=False)
        return items_to_choices(
            [item for item in member.inventory.filter(lambda i: i.openable) if SharkBot.Utils.item_contains(item, current.lower())]
        )

    @staticmethod
    async def member_balance(interaction: Interaction, current: str) -> list[Choice]:
        member = SharkBot.Member.get(interaction.user.id, create=False)
        try:
            current = int(current)
        except ValueError:
            return [
                Choice(
                    name=f"${member.balance} - Balance",
                    value=member.balance
                )
            ]
        if current >= member.balance:
            return [
                Choice(
                    name=f"You don't have ${current}!",
                    value=current
                ),
                Choice(
                    name=f"${member.balance} - Balance",
                    value=member.balance
                )
            ]
        else:
            tens = []
            i = current * 10
            while i < member.balance:
                tens.append(i)
                i *= 10
            return [
                Choice(
                    name=f"${current}",
                    value=current
                )
            ] + balance_to_choices(tens)[0:3] + [
                Choice(
                    name=f"${member.balance} - Balance",
                    value=member.balance
                )
            ]

    @staticmethod
    async def shop_items(interaction: Interaction, current: str) -> list[Choice]:
        current = current.lower()
        results = []
        try:
            for listing in SharkBot.Listing.listings:
                if SharkBot.Utils.item_contains(listing.item, current):
                    results.append(
                        Choice(
                            name=f"{listing.item.name} - ${listing.price}",
                            value=listing.item.id
                        )
                    )
            return results
        except Exception as e:
            print(e)

    @staticmethod
    async def seal(interaction: Interaction, current: str) -> list[Choice]:
        current = current.lower()
        return [
            Choice(
                name=seal_name,
                value=seal_hash
            ) for seal_name, seal_hash in SEAL_HASHES.items() if current in seal_name.lower()
        ][0:10]
