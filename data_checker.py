import SharkBot


def print_items():
    print("-----Items-----")
    for collection in SharkBot.Collection.collections:
        print(f"- {repr(collection)}")
        for item in collection.items:
            print(f"\t- {repr(item)}")
        print("")
    print("")


def print_collections():
    print("-----Collections-----")
    for collection in SharkBot.Collection.collections:
        print(f"- {repr(collection)}")

    print("")


def print_rarities():
    print("-----Rarities-----")
    for rarity in SharkBot.Rarity.rarities:
        print(f"- {repr(rarity)}")

    print("")


print_rarities()
