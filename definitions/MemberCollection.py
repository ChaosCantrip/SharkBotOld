from definitions import Item, SharkErrors
from typing import Union


class MemberCollection:

    def __init__(self, member, itemids: list[str]) -> None:
        self.member = member
        self._items = [Item.get(itemid) for itemid in itemids]

    @property
    def items(self) -> list[Item.Item]:
        return list(self._items)

    @property
    def itemids(self) -> list[str]:
        return [item.id for item in self._items]

    def contains(self, item: Union[Item.Item, str]) -> bool:
        if type(item) is str:
            item = Item.get(item)
        return item in self._items

    def add(self, item: Item.Item) -> None:
        self._items.append(item)

    def remove(self, item: Item.Item) -> None:
        if item not in self._items:
            raise SharkErrors.ItemNotInCollectionError(self.member.id, item.id)
        self._items.remove(item)

    def sort(self) -> None:
        self._items.sort(key=Item.get_order_index)
