import datetime
from dataclasses import dataclass
import SharkBot

@dataclass(frozen=True)
class WellspringWeapon:
    name: str
    type: str

@dataclass(frozen=True)
class WellspringDetails:
    mode: str
    boss: str
    weapon: WellspringWeapon


ROTATION_OFFSET = (datetime.date(2023, 1, 1) - SharkBot.Destiny.season_start).days

class Wellspring:
    pass
