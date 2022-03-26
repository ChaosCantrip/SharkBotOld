class Order():

    def __init__(self, data):
        self.id = data["id"]
        self.email = data["billing"]["email"]