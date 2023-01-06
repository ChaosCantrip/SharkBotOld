import random

from SharkBot import Item, Errors, Response
from typing import Union


class MemberInventory:

    def __init__(self, member, item_ids: list[str]) -> None:
        self.member = member
        self._items = [Item.get(itemid) for itemid in item_ids]

    def __len__(self) -> int:
        return len(self._items)

    @property
    def items(self) -> list[Item.Item]:
        return list(self._items)

    @property
    def item_ids(self) -> list[str]:
        return list([item.id for item in self._items])

    @property
    def lootboxes(self) -> list[Item.Lootbox]:
        return list([item for item in self._items if item.type == "Lootbox"])

    @property
    def lootbox_ids(self) -> list[str]:
        return list([item.id for item in self._items if item.type == "Lootbox"])

    @property
    def unlocked_lootboxes(self) -> list[Item.Lootbox]:
        return list([item for item in self._items if item.type == "Lootbox" and item.unlocked])

    @property
    def unlocked_lootbox_ids(self) -> list[str]:
        return list([item.id for item in self._items if item.type == "Lootbox" and item.unlocked])

    @property
    def locked_lootboxes(self) -> list[Item.Lootbox]:
        return list([item for item in self._items if item.type == "Lootbox" and not item.unlocked])

    @property
    def locked_lootbox_ids(self) -> list[str]:
        return list([item.id for item in self._items if item.type == "Lootbox" and not item.unlocked])

    @property
    def sellable_items(self) -> list[Item.Item]:
        return list([item for item in self._items if item.sellable])

    def count(self, item: Item.Item) -> int:
        return self._items.count(item)

    def __contains__(self, item: Union[Item.Item, str]) -> bool:
        if type(item) is str:
            item = Item.get(item)
        return item in self._items

    def contains(self, item: Union[Item.Item, str]) -> bool:
        if type(item) is str:
            item = Item.get(item)
        return item in self._items

    def add(self, item: Item.Item) -> Response.InventoryAddResponse:
        response = Response.InventoryAddResponse(item=item)
        if item not in self.member.collection:
            self.member.collection.add(item)
            response.new_item = True
        self._items.append(item)
        return response

    def add_items(self, items: list[Item.Item]) -> list[Response.InventoryAddResponse]:
        return [self.add(item) for item in items]

    def remove(self, item: Item.Item) -> None:
        if item not in self._items:
            raise Errors.ItemNotInInventoryError(self.member.id, item.id)
        self._items.remove(item)

    def remove_all(self) -> None:
        self._items = []

    def sort(self) -> None:
        self._items.sort(key=Item.get_order_index)

    def get_duplicates(self, included_types=None) -> list[Union[Item.Item, Item.Lootbox]]:
        if included_types is None:
            included_types = [Item.Item]
        dupes = []
        for item in set(self._items):
            if type(item) not in included_types:
                continue
            count = self.count(item)
            if count > 1:
                dupes += [item] * (count - 1)

        return dupes

    def open_box(self, box: Item.Lootbox, guarantee_new_item: bool = False) -> Response.BoxOpenResponse:
        response = Response.BoxOpenResponse(box=box)
        guarantee_new_item = guarantee_new_item or box.id in Item.guaranteed_new_boxes
        item = box.roll()

        if guarantee_new_item:
            if item in self.member.collection:
                possible_items = list(set(item.collection.items) - set(self.member.collection.items))
                if len(possible_items) > 0:
                    item = random.choice(possible_items)

        response.new_item = item not in self.member.collection
        response.item = item

        self.remove(box)
        self.add(item)

        return response

    def open_boxes(self, to_open: list[tuple[Item.Lootbox, bool]]) -> list[Response.BoxOpenResponse]:
        return [self.open_box(*box) for box in to_open]
