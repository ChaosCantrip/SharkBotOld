import discord
from discord.ext import commands

from definitions import Item, Member


class BuyView(discord.ui.View):
    def __init__(self, boughtItems: list[Item.Lootbox], memberid: int, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boughtItems = boughtItems
        self.member = Member.get(memberid)
        self.embed = embed

    @discord.ui.button(label="Open All")
    async def openall_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.member.id:
            return
        button.disabled = True
        if self.member.inventory.items.count(self.boughtItems[0]) < len(self.boughtItems):
            self.embed.colour = discord.Color.red()
            self.embed.add_field(name="Open All",
                                 value="It looks like the items you bought weren't in your inventory when you tried to open them!")
            await interaction.response.edit_message(embed=self.embed, view=self)
            return
        openedText = ""
        box = self.boughtItems[0]
        for box in self.boughtItems:
            item = box.roll()
            if not self.member.collection.contains(item):
                openedText += f"{item.collection.icon} {item.name} :sparkles:\n"
            else:
                openedText += f"{item.collection.icon} {item.name}\n"
            self.member.inventory.remove(box)
            self.member.inventory.add(item)
        self.embed.add_field(
            name=f"Opened {len(self.boughtItems)}x {box.rarity.icon} {box.name}",
            value=openedText)
        await interaction.response.edit_message(embed=self.embed, view=self)
