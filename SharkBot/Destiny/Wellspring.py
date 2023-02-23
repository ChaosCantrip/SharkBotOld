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


ROTATION_OFFSET = (datetime.date(2023, 1, 1) - SharkBot.Destiny.season_start).days

class Wellspring:
    pass
