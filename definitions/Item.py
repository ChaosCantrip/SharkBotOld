from typing import ItemsView
from definitions import Collection, Rarity, SharkErrors

class Item():
    
    def __init__(self, itemDataString):
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.get(itemData[3])
        self.rarity = Rarity.get(itemData[3])

        Collection.add_item(self)

def get(search: str):
    search = search.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search == item.id:
                return item
    raise SharkErrors.ItemNotFoundError(search)

def search(search: str):
    search = search.upper()
    for collection in Collection.collections:
        for item in collection.items:
            if search == item.id or search == item.name.upper():
                return item
    raise SharkErrors.ItemNotFoundError(search)

items = []

def import_item_file(filename, itemType):
    with open(f"data/collectibles/{filename}", "r") as infile:
        fileData = infile.read()

    for line in fileData.split("\n"):
        if line == "":
            continue
        items.append(itemType(line))

