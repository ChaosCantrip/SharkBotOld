from typing import Optional

import discord

from SharkBot import Item
from .OpenButton import OpenButton


class MissionCompleteView(discord.ui.View):
    def __init__(self, boxes: list[Item.Lootbox], member, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boxes = boxes
        self.member = member
        self.embed = embed
        self.add_item(OpenButton(self.member, self.embed, self.boxes))
        self.message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
