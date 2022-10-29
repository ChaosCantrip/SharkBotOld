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

print_collections()
