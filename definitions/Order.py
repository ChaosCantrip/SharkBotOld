class OrderItem():
    
    def __init__(self, data):
        self.index = data["id"]
        self.product_id = data["product_id"]
        self.product_name = data["name"]
        self.quantity = data["quantity"]

class Order():

    def __init__(self, data):
        self.id = data["id"]
        self.status = data["status"]
        self.email = data["billing"]["email"]