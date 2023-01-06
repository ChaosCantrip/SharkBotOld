import SharkBot

class _Items:

    def __init__(self, items: list[str]):
        self._items: list[SharkBot.Item.Item] = [SharkBot.Item.get(item_id) for item_id in items]

class _Auto:

    def __init__(self, items: list[str]):
        self._items: set[SharkBot.Item.Item] = {SharkBot.Item.get(item_id) for item_id in items}

class MemberVault:

    def __init__(self, items: list[str], auto: list[str]):
        self.items = _Items(items)
        self.auto = _Auto(auto)
