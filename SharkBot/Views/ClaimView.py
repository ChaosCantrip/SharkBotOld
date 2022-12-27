from typing import Optional

import discord

from SharkBot import Item, Member
from .OpenButton import OpenButton


class ClaimView(discord.ui.View):
    def __init__(self, boxes: list[Item.Lootbox], member_id: int, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boxes = boxes
        self.member = Member.get(member_id)
        self.embed = embed
        self.add_item(OpenButton(self.member, self.embed, self.boxes))
        self.message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
