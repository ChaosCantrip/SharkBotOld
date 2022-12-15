import SharkBot


class BoxOpenResponse:

    def __init__(self, box: SharkBot.Item.Lootbox = None, item: SharkBot.Item.Item = None, new_item: bool = False):
        self.box = box
        self.item = item
        self.new_item = new_item

    @property
    def item_printout(self) -> str:
        if self.new_item:
            return f"{str(self.item)} :sparkles:"
        else:
            return str(self.item)
