
table = [
    ["C1", "Manky Toastie", "I... I wouldn't touch that if I were you.", 5]]

class Item():
    
    def __init__(self, itemData):
        self.id, self.name, self.description, self.price = itemData

collection = {}

for item in table:
    collection[item[0]] = Item(item)