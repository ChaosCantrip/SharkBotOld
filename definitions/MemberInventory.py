from definitions import Member, Item, SharkErrors
from typing import Union


class MemberInventory:

    def __init__(self, member: Member.Member, itemids: list[Item.Item]) -> None:
        self.member = member
        self._items = [Item.get(itemid) for itemid in itemids]

    @property
    def items(self):
        return list(self._items)

    @property
    def itemids(self):
        return [item.id for item in self._items]

    def contains(self, item: Union[Item.Item, str]) -> bool:
        if type(item) is str:
            item = Item.get(item)
        return item in self._items

    def add(self, item: Item.Item) -> None:
        if item.id not in self.member.get_collection():
            self.member.add_to_collection(item)
        self._items.append(item)
        self.member.write_data()

    def remove(self, item: Item.Item):
        if item not in self._items:
            raise SharkErrors.ItemNotInInventoryError(self.member.id, item.id)
        self._items.remove(item)
        self.member.write_data()