import SharkBot


def print_items():
    for collection in SharkBot.Collection.collections:
        print(f"- {repr(collection)}")
        for item in collection.items:
            print(f"\t- {repr(item)}")
        print("")
    print("")


def print_collections():
    for collection in SharkBot.Collection.collections:
        print(f"- {repr(collection)}")

    print("")


def print_rarities():
    for rarity in SharkBot.Rarity.rarities:
        print(f"- {repr(rarity)}")

    print("")


print_rarities()
