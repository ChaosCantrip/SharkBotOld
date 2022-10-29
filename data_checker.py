import SharkBot


def print_items():
    for collection in SharkBot.Collection.collections:
        print("- " + repr(collection))
        for item in collection.items:
            print(f"\t- {repr(item)}")
        print("")

print_items()