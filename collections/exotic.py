
table = [
    ["E1", "Luke's Ball", "Without his ball, is he no more than... Luke?", 1000]]

class Item():
    
    def __init__(self, itemData):
        self.id, self.name, self.description, self.price = itemData

collection = {}

for item in table:
    collection[item[0]] = Item(item)
