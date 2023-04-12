from typing import Iterator


class ProfileResponseData:

    def __init__(self, data: dict):
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def get(self, item, default=None):
        return self.data.get(item, default)

    @property
    def items(self) -> Iterator[dict]:
        for item_data in self.data["profileInventory"]["data"]["items"]:
            yield item_data
        for bucket in ["characterInventories", "characterEquipment"]:
            for character in self.data[bucket]["data"].values():
                for item_data in character["items"]:
                    yield item_data

    @property
    def instanced_items(self) -> Iterator[dict]:
        for item in self.items:
            if item.get("itemInstanceId") is not None:
                yield item
