from typing import Self, Optional

from SharkBot.Destiny import Shield, Champion

class NightfallDifficulty:

    def __init__(self, activity_data: dict):
        self.name: str = activity_data["description"]
        self.difficulty: str = activity_data["name"]
        self.light_level: int = activity_data["activityLightLevel"]
        self.destination_hash: int = activity_data["destinationHash"]
        self.modifier_hashes: list[int] = [m["activityModifierHash"] for m in activity_data["modifiers"]]
        self.shield_types = Shield.from_modifiers(self.modifier_hashes)
        self.champion_types = Champion.from_modifiers(self.modifier_hashes)

class Nightfall:

    def __init__(self, name: str):
        self.name = name
        self.adept: Optional[NightfallDifficulty] = None
        self.hero: Optional[NightfallDifficulty] = None
        self.legend: Optional[NightfallDifficulty] = None
        self.master: Optional[NightfallDifficulty] = None
        self.grandmaster: Optional[NightfallDifficulty] = None