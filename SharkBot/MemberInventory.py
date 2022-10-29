from SharkBot import Item, Errors
from typing import Union


class MemberInventory:

    def __init__(self, member, item_ids: list[str]) -> None:
        self.member = member
        self._items = [Item.get(itemid) for itemid in item_ids]

    @property
    def items(self) -> list[Item.Item]:
        return list(self._items)

    @property
    def item_ids(self) -> list[str]:
        return [item.id for item in self._items]

    @property
    def lootboxes(self) -> list[Item.Lootbox]:
        return [item for item in self._items if type(item) is Item.Lootbox]

    @property
    def lootbox_ids(self) -> list[str]:
        return [item.id for item in self._items if type(item) is Item.Lootbox]

    def count(self, item: Item.Item) -> int:
        return self._items.count(item)

    def contains(self, item: Union[Item.Item, str]) -> bool:
        if type(item) is str:
            item = Item.get(item)
        return item in self._items

    def add(self, item: Item.Item) -> None:
        if not self.member.collection.contains(item):
            self.member.collection.add(item)
        self._items.append(item)

    def remove(self, item: Item.Item) -> None:
        if item not in self._items:
            raise Errors.ItemNotInInventoryError(self.member.id, item.id)
        self._items.remove(item)

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
