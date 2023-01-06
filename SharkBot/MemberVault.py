import SharkBot

class MemberVault:

    def __init__(self, items: list[str], auto: list[str]):
        self._items: list[SharkBot.Item.Item] = [SharkBot.Item.get(item_id) for item_id in items]
        self._auto: set[SharkBot.Item.Item] = {SharkBot.Item.get(item_id) for item_id in auto}
