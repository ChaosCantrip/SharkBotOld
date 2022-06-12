import json

allItems = []

def importFile(collectionName, collectionImage, collectionFile):
    collection = {}
    collection["name"] = collectionName
    collection["image"] = collectionImage
    with open(collectionFile, "r") as infile:
        fileData = infile.read()
        fileLines = fileData.split("\n")
        items = []
        for line in fileLines:
            lineData = line.split("|")
            item = {}
            item["id"] = lineData[0]
            item["name"] = lineData[1]
            item["description"] = lineData[2]
            items.append(item)
        collection["items"] = items
    allItems.append(collection)

importFile("Common", "common_icon.png", "common.txt")
importFile("Uncommon", "uncommon_icon.png", "uncommon.txt")
importFile("Rare", "rare_icon.png", "rare.txt")
importFile("Legendary", "legendary_icon.png", "legendary.txt")
importFile("Exotic", "exotic_icon.png", "exotic.txt")
importFile("Mythic", "mythic_icon.png", "mythic.txt")
importFile("Lootboxes", "lootboxes_icon.png", "lootboxes.txt")
importFile("Valentines", "valentines_icon.png", "valentines.txt")
importFile("Witch Queen", "witch_queen_icon.png", "witch_queen.txt")
importFile("Easter", "easter_icon.png", "easter.txt")

print(allItems)

with open("items.json", "w") as outfile:
    json.dump(allItems, outfile)
print("Done!")
