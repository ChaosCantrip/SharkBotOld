from definitions import Member, Item


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