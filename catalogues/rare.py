
table = [
    ["R1", "SharkBot Bug", "Oh fuck, not again", 100]]

class Item():
    
    def __init__(self, itemData):
        self.id, self.name, self.description, self.price = itemData

collection = {}

for item in table:
    collection[item[0]] = Item(item)
