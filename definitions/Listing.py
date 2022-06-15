from definitions import Item

class Listing():

    def __init__(self, listingDataString):
        listingData = listingDataString.split(":")
        self.item = Item.get(listingData[0])
        self.price = int(listingData[1])

listings = []
availableItems = []

with open("data/collectibles/shop.txt", "r") as infile:
    fileData = infile.read()

for line in fileData.split("\n"):
    if line == "":
        continue
    listing = Listing(line)
    listings.append(listing)
    availableItems.append(listing.item)