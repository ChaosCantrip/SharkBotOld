from typing import Optional

import discord

from SharkBot import Item, Member
from .OpenButton import OpenButton


class BuyView(discord.ui.View):
    def __init__(self, bought_items: list[Item.Lootbox], member_id: int, embed: discord.Embed, timeout=180):
        super().__init__(timeout=timeout)
        self.boughtItems = bought_items
        self.member = Member.get(member_id)
        self.embed = embed
        self.add_item(OpenButton(self.member, self.embed, self.boughtItems))
        self.message: Optional[discord.Message] = None

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
