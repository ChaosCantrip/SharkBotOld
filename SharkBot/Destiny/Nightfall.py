class NightfallDifficulty:

    def __init__(self, activity_data: dict):
        self.name = activity_data["description"]
        self.difficulty = activity_data["name"]
        self.light_level: int = activity_data["activityLightLevel"]
        self.destination_hash: int = activity_data["destinationHash"]
        self.modifier_hashes: list[int] = [m["activityModifierHash"] for m in activity_data["modifiers"]]

class Nightfall:
    pass