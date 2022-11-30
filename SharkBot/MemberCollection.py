from SharkBot import Item, Errors
from typing import Union


class MemberCollection:

    def __init__(self, member, item_ids: list[str]) -> None:
        self.member = member
        self._items = [Item.get(itemid) for itemid in item_ids]
        self._xp_value = -1
        self._old_xp_value = self.xp_value

    def __len__(self) -> int:
        return len(self._items)

    @property
    def items(self) -> list[Item.Item]:
        return list(self._items)

    @property
    def item_ids(self) -> list[str]:
        return [item.id for item in self._items]

    def contains(self, item: Union[Item.Item, str]) -> bool:
        if type(item) is str:
            item = Item.get(item)
        return item in self._items

    def add(self, item: Item.Item) -> None:
        self._items.append(item)
        self._xp_value = -1

    def remove(self, item: Item.Item) -> None:
        if item not in self._items:
            raise Errors.ItemNotInCollectionError(self.member.id, item.id)
        self._items.remove(item)
        self._xp_value = -1

    def sort(self) -> None:
        self._items.sort(key=Item.get_order_index)

    @property
    def xp_value(self) -> int:
        if self._xp_value == -1:
            self._xp_value = sum([item.xp_value for item in self.items])
        return self._xp_value

    @property
    def xp_value_changed(self) -> bool:
        return self.xp_value == self._old_xp_value
