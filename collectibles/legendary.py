
table = [
    ["L1", "Gift Sub", "Thank you DiscountMando for the gift sub!!", 500]]

class Item():
    
    def __init__(self, itemData):
        self.id, self.name, self.description, self.price = itemData

collection = {}

for item in table:
    collection[item[0]] = Item(item)
