import discord
from definitions import Item


class SellButton(discord.ui.Button):
    def __init__(self, member, embed: discord.Embed, items: list[Item.Item], label="Sell All",
                 **kwargs):
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
