from typing import Self, Optional

from SharkBot.Destiny import Shield, Champion, Errors

class NightfallDifficulty:

    def __init__(self, activity_data: dict):
        self.name: str = activity_data["description"]
        self.difficulty: str = activity_data["name"]
        self.light_level: int = activity_data["activityLightLevel"]
        self.destination_hash: int = activity_data["destinationHash"]
        self.modifier_hashes: list[int] = [m["activityModifierHash"] for m in activity_data["modifiers"]]
        self.shield_types = Shield.from_modifiers(self.modifier_hashes)
        self.champion_types = Champion.from_modifiers(self.modifier_hashes)

    def register(self):
        if self.name not in Nightfall.nightfalls_dict:
            Nightfall.nightfalls_dict[self.name] = Nightfall(self.name)
        nightfall = Nightfall.nightfalls_dict[self.name]
        if self.difficulty.endswith("Adept"):
            nightfall.adept = self
        elif self.difficulty.endswith("Hero"):
            nightfall.hero = self
        elif self.difficulty.endswith("Legend"):
            nightfall.legend = self
        elif self.difficulty.endswith("Master"):
            nightfall.master = self
        elif self.difficulty.endswith("Grandmaster"):
            nightfall.grandmaster = self
        else:
            raise KeyError

class Nightfall:
    nightfalls_dict: dict[str, Self] = {}

    def __init__(self, name: str):
        self.name = name
        self.adept: Optional[NightfallDifficulty] = None
        self.hero: Optional[NightfallDifficulty] = None
        self.legend: Optional[NightfallDifficulty] = None
        self.master: Optional[NightfallDifficulty] = None
        self.grandmaster: Optional[NightfallDifficulty] = None

    @classmethod
    def get(cls, search: str):
        try:
            return cls.nightfalls_dict[search]
        except KeyError:
            raise Errors.NightfallNotFoundError(search)