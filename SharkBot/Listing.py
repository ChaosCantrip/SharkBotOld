from SharkBot import Item


class Listing:

    def __init__(self, listingDataString: str) -> None:
        listingData = listingDataString.split(":")
        self.item = Item.get(listingData[0])
        self.price = int(listingData[1])


listings: list[Listing] = []
availableItems: list[Item] = []


def load_listings() -> None:
    global listings
    global availableItems

    with open("data/static/collectibles/shop.txt", "r") as infile:
        fileData = infile.read()

    lines = [line for line in fileData.split("\n") if line != ""]
    listings = [Listing(line) for line in lines]
    availableItems = [listing.item for listing in listings]


load_listings()
