class Order():

    def __init__(self, data):
        self.id = data["id"]
        self.status = data["status"]
        self.email = data["billing"]["email"]