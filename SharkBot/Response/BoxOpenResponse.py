import SharkBot


class BoxOpenResponse:

    def __init__(self, box: SharkBot.Item.Lootbox, item: SharkBot.Item.Item, new_item: bool):
        self.box = box
        self.item = item
        self.new_item = new_item
