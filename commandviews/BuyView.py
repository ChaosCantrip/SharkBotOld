import discord
from discord.ext import commands

from definitions import Item, Member


class BuyView(discord.ui.View):
    def __init__(self, boughtItems: list[Item.Lootbox], memberid: int, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boughtItems = boughtItems
        self.memberid = memberid
        self.embed = embed

    @discord.ui.button(label="Open All")
    async def openall_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = Member.get(self.memberid)
        button.disabled = True
        if member.inventory.count(self.boughtItems[0].id) < len(self.boughtItems):
            self.embed.color = discord.Color.red()
            self.embed.add_field(name="Open All",
                                 value="It looks like the items you bought weren't in your inventory when you tried to open them!")
            await interaction.response.edit_message(embed=self.embed, view=self)
            return
        openedText = ""
        box = self.boughtItems[0]
        for box in self.boughtItems:
            item = box.roll()
            if item.id in member.get_inventory():
                openedText += f"{item.collection.get_icon(interaction.guild)} {item.name} :sparkles:\n"
            else:
                openedText += f"{item.collection.get_icon(interaction.guild)} {item.name}\n"
            member.remove_from_inventory(box)
            member.add_to_inventory(item)
        self.embed.add_field(
            name=f"Opened {len(self.boughtItems)}x {box.rarity.get_icon(interaction.guild)} {box.name}",
            value=openedText)
        await interaction.response.edit_message(embed=self.embed, view=self)
