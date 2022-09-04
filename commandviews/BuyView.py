import discord
from discord.ext import commands

from definitions import Item, Member


class BuyView(discord.ui.View):
    def __init__(self, boughtItems: list[Item.Lootbox], memberid: int, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boughtItems = boughtItems
        self.member = Member.get(memberid)
        self.embed = embed
        self.add_item(OpenButton(self.member, self.embed, self.boughtItems))


class OpenButton(discord.ui.Button):
    def __init__(self, member: Member.Member, embed: discord.Embed, boxes: list[Item.Lootbox], label="Open All", **kwargs):
        super().__init__(label=label, **kwargs)
        self.member = member
        self.embed = embed
        self.boxes = boxes

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.member.id:
            return

        self.disabled = True
        box = self.boxes[0]

        if self.member.inventory.items.count(box) < len(self.boxes):
            self.embed.add_field(
                name="Open All Failed",
                value="It looks like the boxes aren't in your inventory any more!",
                inline=False
            )
            self.embed.colour = discord.Colour.red()
            await interaction.response.edit_message(embed=self.embed, view=self.view)
            return

        openedItems = [box.roll() for box in self.boxes]
        for item in openedItems:
            self.member.inventory.remove(box)
            self.member.inventory.add(item)

        self.embed.add_field(
            name=f"Opened {len(openedItems)}x {box.rarity.icon} {box.name}",
            value="\n".join(
                [f"{item.rarity.icon} {item.name}{' :sparkles:' if not self.member.inventory.contains(item) else ''}"
                 for item in openedItems]
            ),
            inline=False
        )

        self.view.add_item(SellButton(self.member, self.embed, openedItems))
        await interaction.response.edit_message(embed=self.embed, view=self.view)

        self.member.write_data()


class SellButton(discord.ui.Button):
    def __init__(self, member: Member.Member, embed: discord.Embed, items: list[Item.Item], label="Sell All", **kwargs):
        super().__init__(label=label, **kwargs)
        self.member = member
        self.embed = embed
        self.items = items

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.member.id:
            return

        self.disabled = True

        if not all([self.member.inventory.contains(item) for item in self.items]):
            self.embed.add_field(
                name="Sell All Failed",
                value="It looks like the items aren't in your inventory any more!",
                inline=False
            )
            self.embed.colour = discord.Colour.red()
            await interaction.response.edit_message(embed=self.embed, view=self.view)
            return

        value = sum([item.get_value() for item in self.items])

        for item in self.items:
            self.member.inventory.remove(item)

        self.member.add_balance(value)

        self.embed.add_field(
            name=f"Sell all",
            value=f"Sold {len(self.items)} items for ${value}. Your new balance is ${self.member.get_balance()}",
            inline=False
        )
        await interaction.response.edit_message(embed=self.embed, view=self.view)

        self.member.write_data()
