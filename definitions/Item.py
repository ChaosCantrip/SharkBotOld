class Item():
    
    def __init__(self, itemDataString):
        itemData = itemDataString.split("|")
        self.id = itemData[0]
        self.description = itemData[1]
        self.collection = itemData[2]
        self.rarity = itemData[3]
