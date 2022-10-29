from SharkBot import Item


class Listing:

    def __init__(self, item_id: str, price_str: str) -> None:
        self.item = Item.get(item_id)
        self.price = int(price_str)

    def __repr__(self) -> str:
        return f"Listing[item='{self.item.id} ({self.item.name}), price='${self.price}']"


listings: list[Listing] = []
availableItems: list[Item] = []


def load_listings() -> None:
    global listings
    global availableItems

    with open("data/static/collectibles/shop.txt", "r") as infile:
        file_data = infile.read()

    lines = [line for line in file_data.split("\n") if line != ""]
    listings = [Listing(*line.split(":")) for line in lines]
    availableItems = [listing.item for listing in listings]


load_listings()
