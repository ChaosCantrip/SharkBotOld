from typing import Optional

import SharkBot
from .InventoryAddResponse import InventoryAddResponse


class BoxOpenResponse:

    def __init__(
            self,
            box: SharkBot.Item.Lootbox = None,
            item: SharkBot.Item.Item = None,
            new_item: bool = False,
            auto_vault: bool = False,
            clover_used: bool = False,
            dice_used: bool = False,
            inv_response: Optional[InventoryAddResponse] = None
    ):
        self.box = box
        self.item = item
        self.new_item = new_item
        self.auto_vault = auto_vault
        self.clover_used = clover_used
        self.dice_used = dice_used
        if inv_response is not None:
            self.item = inv_response.item
            self.new_item = inv_response.new_item
            self.auto_vault = inv_response.auto_vault
            self.clover_used = inv_response.clover_used
            self.dice_used = inv_response.dice_used

    def import_flags(self, response: InventoryAddResponse):
        self.item = response.item if response.item is not None else self.item
        self.new_item = response.new_item if response.new_item is not None else self.new_item
        self.auto_vault = response.auto_vault if response.auto_vault is not None else self.auto_vault
        self.clover_used = response.clover_used if response.clover_used is not None else self.clover_used
        self.dice_used = response.dice_used if response.dice_used is not None else self.dice_used

    @property
    def flags(self) -> list[str]:
        _flags = []
        if self.new_item:
            _flags.append(":sparkles:")
        if self.auto_vault:
            _flags.append(":gear:")
        if self.clover_used:
            _flags.append(":four_leaf_clover:")
        if self.dice_used:
            _flags.append(":game_die:")
        return _flags

    @property
    def item_printout(self) -> str:
        return str(self.item) + " " + " ".join(self.flags)
