class Rarity():
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

common = Rarity("Common", 5)
uncommon = Rarity("Uncommon", 10)
rare = Rarity("Rare", 20)
legendary = Rarity("Legendary", 50)
exotic = Rarity("Exotic", 150)
mythic = Rarity("Mythic", 500)

lootboxes = Rarity("Lootboxes", 100)

valentines = Rarity("Valentines", 10)
witch_queen = Rarity("Witch Queen", 10)
easter = Rarity("Easter", 10)

rarities = [common, uncommon, rare, legendary, exotic, lootboxes, mythic, valentines, witch_queen, easter]
