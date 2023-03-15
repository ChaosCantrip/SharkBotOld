from . import Enums
from SharkBot import Icon

class Guardian:

    def __init__(self, definition: dict):
        self.race = Enums.GuardianRace(definition["raceType"]).name.title()
        self.type = Enums.GuardianClass(definition["classType"]).name.title()

    @property
    def icon(self) -> str:
        return Icon.get(f"class_{self.type.lower()}")

    def __str__(self):
        return f"{self.icon} {self.race} {self.type}"