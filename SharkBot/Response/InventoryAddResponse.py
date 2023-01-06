import SharkBot


class InventoryAddResponse:

    def __init__(self, item: SharkBot.Item.Item = None, new_item: bool = False, auto_vault: bool = False):
        self.item = item
        self.new_item = new_item
        self.auto_vault = auto_vault

    @property
    def flags(self) -> list[str]:
        _flags = []
        if self.new_item:
            _flags.append(":sparkles:")
        if self.auto_vault:
            _flags.append(":gear:")
        return _flags

    @property
    def item_printout(self) -> str:
        return str(self.item) + " " + " ".join(self.flags)
