from definitions import Collection

class Item():
    
    def __init__(self, itemDataString):
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.name = itemData[1]
        self.description = itemData[2]
        self.collection = Collection.get(itemData[3])
        self.rarity = itemData[3]

        Collection.add_item(self)
