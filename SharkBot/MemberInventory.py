import random

import SharkBot
from typing import Union


class MemberInventory:

    def __init__(self, member, item_ids: list[str]) -> None:
        self.member: SharkBot.Member.Member = member
        self._items = [SharkBot.Item.get(itemid) for itemid in item_ids]

    def __len__(self) -> int:
        return len(self._items)

    @property
    def items(self) -> list[SharkBot.Item.Item]:
        return list(self._items)

    @property
    def item_ids(self) -> list[str]:
        return list([item.id for item in self._items])

    @property
    def lootboxes(self) -> list[SharkBot.Item.Lootbox]:
        return list([item for item in self._items if item.type == "Lootbox"])

    @property
    def lootbox_ids(self) -> list[str]:
        return list([item.id for item in self._items if item.type == "Lootbox"])

    @property
    def unlocked_lootboxes(self) -> list[SharkBot.Item.Lootbox]:
        return list([item for item in self._items if item.type == "Lootbox" and item.unlocked])

    @property
    def unlocked_lootbox_ids(self) -> list[str]:
        return list([item.id for item in self._items if item.type == "Lootbox" and item.unlocked])

    @property
    def locked_lootboxes(self) -> list[SharkBot.Item.Lootbox]:
        return list([item for item in self._items if item.type == "Lootbox" and not item.unlocked])

    @property
    def locked_lootbox_ids(self) -> list[str]:
        return list([item.id for item in self._items if item.type == "Lootbox" and not item.unlocked])

    @property
    def sellable_items(self) -> list[SharkBot.Item.Item]:
        return list([item for item in self._items if item.sellable])

    def count(self, item: SharkBot.Item.Item) -> int:
        return self._items.count(item)

    def __contains__(self, item: Union[SharkBot.Item.Item, str]) -> bool:
        if type(item) is str:
            item = SharkBot.Item.get(item)
        return item in self._items

    def contains(self, item: Union[SharkBot.Item.Item, str]) -> bool:
        if type(item) is str:
            item = SharkBot.Item.get(item)
        return item in self._items

    def add(self, item: SharkBot.Item.Item, ignore_vault: bool = False) -> SharkBot.Response.InventoryAddResponse:
        response = SharkBot.Response.InventoryAddResponse(item=item)
        if item not in self.member.collection:
            self.member.collection.add(item)
            response.new_item = True
        if not ignore_vault and item in self.member.vault.auto:
            self.member.vault.add(item)
            response.auto_vault = True
        else:
            self._items.append(item)
        return response

    def add_items(self, items: list[SharkBot.Item.Item], ignore_vault: bool = False) -> list[SharkBot.Response.InventoryAddResponse]:
        return [self.add(item, ignore_vault) for item in items]

    def remove(self, item: SharkBot.Item.Item) -> None:
        if item not in self._items:
            raise SharkBot.Errors.ItemNotInInventoryError(self.member.id, item.id)
        self._items.remove(item)

    def remove_all(self) -> None:
        self._items = []

    def sort(self) -> None:
        self._items.sort(key=SharkBot.Item.get_order_index)

    def get_duplicates(self, included_types=None) -> list[Union[SharkBot.Item.Item, SharkBot.Item.Lootbox]]:
        if included_types is None:
            included_types = [SharkBot.Item.Item]
        dupes = []
        for item in set(self._items):
            if type(item) not in included_types:
                continue
            count = self.count(item)
            if count > 1:
                dupes += [item] * (count - 1)

        return dupes

    def open_box(self, box: SharkBot.Item.Lootbox, guarantee_new_item: bool = False) -> SharkBot.Response.BoxOpenResponse:
        guarantee_new_item = guarantee_new_item or box.id in SharkBot.Item.guaranteed_new_boxes
        loaded_dice = self.member.has_effect("Loaded Dice") and not guarantee_new_item
        loaded_dice_used = False
        item = box.roll()

        if guarantee_new_item or loaded_dice:
            if item in self.member.collection:
                possible_items = list(set(item.collection.items) - set(self.member.collection.items))
                if len(possible_items) > 0:
                    loaded_dice_used = loaded_dice
                    item = random.choice(possible_items)

        self.remove(box)
        inv_response = self.add(item)
        if loaded_dice_used:
            inv_response.dice_used = True
            self.member.effects.use_charge("Loaded Dice")
        response = SharkBot.Response.BoxOpenResponse(box=box, inv_response=inv_response)

        return response

    def open_boxes(self, to_open: list[tuple[SharkBot.Item.Lootbox, bool]]) -> list[SharkBot.Response.BoxOpenResponse]:
        return [self.open_box(*box) for box in to_open]
