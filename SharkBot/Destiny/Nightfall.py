from typing import Self, Optional

from SharkBot.Destiny import Shield, Champion, Errors, Manifest, get_week_index, get_rotation_from

destination_definitions: dict[str, dict] = Manifest.get_definitions_file("DestinyDestinationDefinition")

class NightfallDifficulty:

    def __init__(self, activity_data: dict):
        self.name: str = activity_data["displayProperties"]["description"]
        self.difficulty: str = activity_data["displayProperties"]["name"]
        self._destination_hash: int = activity_data["destinationHash"]
        self.modifier_hashes: list[int] = [m["activityModifierHash"] for m in activity_data["modifiers"]]
        self.shield_types = Shield.from_modifiers(self.modifier_hashes)
        self.champion_types = Champion.from_modifiers(self.modifier_hashes)

    def register(self):
        if self.name not in Nightfall.nightfalls_dict:
            Nightfall.nightfalls_dict[self.name] = Nightfall(self.name, str(self._destination_hash))
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
    def icons(self) -> list[str]:
        return [s.icon for s in self.shield_types] + [c.icon for c in self.champion_types]

    @property
    def data(self) -> dict:
        return {
            "name": self.name,
            "difficulty": self.difficulty,
            "modifier_hashes": self.modifier_hashes,
            "shield_types": [repr(shield) for shield in self.shield_types],
            "champion_types": [repr(champion) for champion in self.champion_types]
        }

class Nightfall:
    nightfalls_dict: dict[str, Self] = {}
    current_rotation: list[Self] = []

    def __init__(self, name: str, destination_hash: str, is_current: bool = False):
        self.name = name
        self.adept: Optional[NightfallDifficulty] = None
        self.hero: Optional[NightfallDifficulty] = None
        self.legend: Optional[NightfallDifficulty] = None
        self.master: Optional[NightfallDifficulty] = None
        self.grandmaster: Optional[NightfallDifficulty] = None
        self.destination_hash = destination_hash
        self.destination: str = destination_definitions[str(self.destination_hash)]["displayProperties"]["name"]
        self.is_current = is_current

    def __repr__(self):
        return f"Nightfall[{self.name}]"

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

    @classmethod
    def get_current(cls) -> Self:
        return cls.current_rotation[get_week_index() % len(cls.current_rotation)]

    @classmethod
    def rotation_from(cls, start_at) -> list[Self]:
        _index = cls.current_rotation.index(start_at)
        return get_rotation_from(cls.current_rotation, _index)

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

conqueror_definition = Manifest.get_definitions_file("DestinyPresentationNodeDefinition")["3776992251"]
record_definitions: dict[str, dict] = Manifest.get_definitions_file("DestinyRecordDefinition")
for record in conqueror_definition["children"]["records"]:
    record_definition = record_definitions[str(record["recordHash"])]
    if record_definition["forTitleGilding"]:
        Nightfall.current_rotation.append(Nightfall.nightfalls_dict[record_definition["displayProperties"]["name"][13:]])

for nightfall in Nightfall.current_rotation:
    nightfall.is_current = True
