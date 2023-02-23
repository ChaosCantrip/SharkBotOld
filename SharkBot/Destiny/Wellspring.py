import datetime
from dataclasses import dataclass
import SharkBot

@dataclass(frozen=True)
class WellspringWeapon:
    name: str
    type: str

@dataclass
class WellspringDetails:
    mode: str
    boss: str
    weapon: WellspringWeapon | dict

    def __post_init__(self):
        self.weapon = WellspringWeapon(**self.weapon)

@dataclass
class WellspringData:
    rotation_start: dict[str, int]
    rotation: list[WellspringDetails]

    def __post_init__(self):
        wellspring_details: dict[str, str | dict[str, str]]
        self.rotation = [WellspringDetails(**wellspring_details) for wellspring_details in self.rotation]


ROTATION_OFFSET = (datetime.date(2023, 1, 1) - SharkBot.Destiny.season_start).days

class Wellspring:
    pass
