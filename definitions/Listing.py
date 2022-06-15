class Listing():

    def __init__(self, listingDataString):
        listingData = listingDataString.split(":")
        self.item = search_for_item(listingData[0])
        self.price = int(listingData[1])

listings = []

with open("data/collectibles/shop.txt", "r") as infile:
    fileData = infile.read()

for line in fileData.split("\n"):
    if line == "":
        continue
    listings.append(Listing(line))