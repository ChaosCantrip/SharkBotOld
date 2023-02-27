from typing import Self, Optional

from SharkBot.Destiny import Shield, Champion, Errors, Manifest

class NightfallDifficulty:

    def __init__(self, activity_data: dict):
        self.name: str = activity_data["displayProperties"]["description"]
        self.difficulty: str = activity_data["displayProperties"]["name"]
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

    @property
    def data(self) -> dict:
        return {
            "name": self.name,
            "difficulty": self.difficulty,
            "light_level": self.light_level,
            "destination_hash": self.destination_hash,
            "modifier_hashes": self.modifier_hashes,
            "shield_types": [repr(shield) for shield in self.shield_types],
            "champion_types": [repr(champion) for champion in self.champion_types]
        }

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

    @property
    def data(self) -> dict:
        return {
            "name": self.name,
            "adept": None if self.adept is None else self.adept.data,
            "hero": None if self.hero is None else self.hero.data,
            "legend": None if self.legend is None else self.legend.data,
            "master": None if self.master is None else self.master.data,
            "grandmaster": None if self.grandmaster is None else self.grandmaster.data
        }

activity_definitions = Manifest.get_definitions_file("DestinyActivityDefinition")
vanguard_ops_definition = Manifest.get_definitions_file("DestinyActivityGraphDefinition")["3129078390"]
vanguard_nodes = {
    str(d["nodeId"]): d for d in vanguard_ops_definition["nodes"]
}
grandmaster_node = vanguard_nodes["3626452082"]
nightfall_node = vanguard_nodes["3160621859"]
grandmaster_activity_hashes: list[str] = [str(d["activityHash"]) for d in grandmaster_node["activities"]]
nightfall_activity_hashes: list[str] = [str(d["activityHash"]) for d in nightfall_node["activities"]]
activity_hashes = nightfall_activity_hashes + grandmaster_activity_hashes
for activity_hash in activity_hashes:
    nightfall_difficulty = NightfallDifficulty(activity_definitions[activity_hash])
    nightfall_difficulty.register()