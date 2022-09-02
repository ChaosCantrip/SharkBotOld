import discord
from discord.ext import commands

from definitions import Item, Member


class ClaimView(discord.ui.View):
    def __init__(self, boxes: list[Item.Lootbox], memberid: int, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boxes = boxes
        self.member = Member.get(memberid)
        self.embed = embed

    @discord.ui.button(label="Open All")
    async def openall_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        if not all(box in self.member.inventory.lootboxes for box in self.boxes):
            self.embed.colour = discord.Color.red()
            self.embed.add_field(name="Open All",
                                 value="It looks like the boxes you claimed weren't in your inventory when you tried to open them!")
            await interaction.response.edit_message(embed=self.embed, view=self)
            return
        else:
            self.embed.add_field(
                name="**Open All**",
                value="==========================",
                inline=False
            )
            for box in self.boxes:
                item = box.roll()
                if not self.member.collection.contains(item):
                    openedText = f"You got :sparkles: {item.collection.icon} {item.name} :sparkles:"
                else:
                    openedText = f"You got {item.collection.icon} {item.name}!"
                self.member.inventory.remove(box)
                self.member.inventory.add(item)
                self.embed.add_field(
                    name=f"Opened {box.rarity.icon} {box.name}",
                    value=openedText,
                    inline=False
                )
        await interaction.response.edit_message(embed=self.embed, view=self)
