import SharkBot

class _Items:

    def __init__(self, items: list[str]):
        self._items: list[SharkBot.Item.Item] = [SharkBot.Item.get(item_id) for item_id in items]

    def __iter__(self):
        return (item for item in self._items)

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def add(self, *items: SharkBot.Item.Item):
        self._items += items

    def remove(self, *items: SharkBot.Item.Item):
        _items = self._items
        try:
            for item in items:
                _items.remove(item)
            self._items = _items
        except ValueError:
            raise SharkBot.Errors.ItemNotInVaultError(items)

    def remove_all(self):
        self._items = []

    def count(self, item: SharkBot.Item.Item) -> int:
        return self._items.count(item)

    @property
    def data(self) -> list[str]:
        return list(item.id for item in self._items)

class _Auto:

    def __init__(self, items: list[str]):
        self._items: set[SharkBot.Item.Item] = {SharkBot.Item.get(item_id) for item_id in items}

    def __iter__(self):
        return (item for item in self._items)

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def add(self, *items: SharkBot.Item.Item):
        self._items.update(items)

    def remove(self, *items: SharkBot.Item.Item):
        _items = self._items
        try:
            for item in items:
                _items.remove(item)
            self._items = _items
        except KeyError:
            raise SharkBot.Errors.ItemNotInVaultError(items)

    def remove_collection(self, collection: SharkBot.Collection.Collection):
        self._items -= set(collection.items)

    def clear(self):
        self._items = set()

    def flag(self, item: SharkBot.Item.Item):
        if item in self._items:
            return " :gear:"
        else:
            return ""

    @property
    def data(self) -> list[str]:
        return list(item.id for item in self._items)

class MemberVault:

    def __init__(self, items: list[str], auto: list[str]):
        self.items = _Items(items)
        self.auto = _Auto(auto)

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def add(self, *items: SharkBot.Item.Item):
        self.items.add(*items)

    def remove(self, *items: SharkBot.Item.Item):
        self.items.remove(*items)

    def remove_all(self):
        self.items.remove_all()

    def count(self, item: SharkBot.Item.Item) -> int:
        return self.items.count(item)

    @property
    def data(self) -> dict[str, list[str]]:
        return {
            "items": self.items.data,
            "auto": self.auto.data
        }