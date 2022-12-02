import discord
from SharkBot import Item
from .SellButton import SellButton


class OpenButton(discord.ui.Button):
    def __init__(self, member, embed: discord.Embed, boxes: list[Item.Lootbox], label="Open All",
                 **kwargs):
        super().__init__(label=label, **kwargs)
        self.member = member
        self.embed = embed
        self.boxes = boxes

    async def callback(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.member.id:
            await interaction.response.defer()
            return

        self.disabled = True

        if any([self.member.inventory.items.count(box) < self.boxes.count(box) for box in set(self.boxes)]):
            self.embed.add_field(
                name="Open All Failed",
                value="It looks like the boxes aren't in your inventory any more!",
                inline=False
            )
            self.embed.colour = discord.Colour.red()
            await interaction.response.edit_message(embed=self.embed, view=self.view)
            return

        all_opened_items = []
        for box, count in {box: self.boxes.count(box) for box in set(self.boxes)}.items():
            opened_items = [boxToOpen.roll() for boxToOpen in [box] * count]
            all_opened_items += opened_items

            for item in opened_items:
                self.member.inventory.remove(box)
                self.member.inventory.add(item)
                self.member.stats.openedBoxes += 1

            self.embed.add_field(
                name=f"Opened {count}x {str(box)}",
                value="\n".join(
                    [f"{str(item)}{':sparkles:' if not self.member.collection.contains(item) else ''}"
                        for item in opened_items]
                ),
                inline=False
            )

        self.view.add_item(SellButton(self.member, self.embed, all_opened_items))
        if len(self.embed.fields[-1].value) < 1000:
            await interaction.response.edit_message(embed=self.embed, view=self.view)
        else:
            self.embed.remove_field(-1)
            self.embed.add_field(
                name="Open All",
                value="Ok so I did open your items, but that made the embed text too long so just trust me!",
                inline=False
            )
            await interaction.response.edit_message(embed=self.embed, view=self.view)

        self.member.write_data()
