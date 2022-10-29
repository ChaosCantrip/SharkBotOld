import SharkBot


def print_items():
    print("-----Items-----")
    for item in SharkBot.Item.items:
        print(f"- {repr(item)}")
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


def print_listings():
    print("-----Listings-----")
    for listing in SharkBot.Listing.listings:
        print(repr(listing))
    print("")


if __name__ == "__main__":
    while True:
        print("-----Menu-----")
        print("1: Items")
        print("2: Collections")
        print("3: Rarities")
        print("4: Listings")
        print("0: Exit")
        choice = input(">> ")
        print("")
        if choice == "0":
            quit()
        elif choice == "1":
            print_items()
        elif choice == "2":
            print_collections()
        elif choice == "3":
            print_rarities()
        elif choice == "4":
            print_listings()
        else:
            print("Invalid Choice! \n")
