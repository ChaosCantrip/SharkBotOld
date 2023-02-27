class NightfallDifficulty:

    def __init__(self, activity_data: dict):
        self.modifier_hashes: list[int] = [m["activityModifierHash"] for m in activity_data["modifiers"]]

class Nightfall:
    pass