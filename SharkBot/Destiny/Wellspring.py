import datetime
from dataclasses import dataclass
import SharkBot

@dataclass
class WellspringWeapon:
    name: str
    type: str
    ammo: SharkBot.Destiny.AmmoType | str
    energy: SharkBot.Destiny.Shield | str

    def __post_init__(self):
        self.ammo = SharkBot.Destiny.AmmoType.get(self.ammo)
        self.energy = SharkBot.Destiny.Shield.get(self.energy)

@dataclass
class WellspringDetails:
    mode: str
    boss: str
    weapon: WellspringWeapon | dict

    def __post_init__(self):
        self.weapon = WellspringWeapon(**self.weapon)

@dataclass
class WellspringData:
    rotation_start: datetime.datetime | dict[str, int]
    rotation: list[WellspringDetails]

    def __post_init__(self):
        wellspring_details: dict[str, str | dict[str, str]]
        self.rotation = [WellspringDetails(**wellspring_details) for wellspring_details in self.rotation]
        self.rotation_start = datetime.datetime(**self.rotation_start)

WELLSPRING_DATA = WellspringData(**SharkBot.Utils.JSON.load("data/static/destiny/wellspring_rotation.json"))

class Wellspring:

    @classmethod
    def get_current(cls) -> WellspringDetails:
        return WELLSPRING_DATA.rotation[SharkBot.Destiny.get_day_index(relative_to=WELLSPRING_DATA.rotation_start) % 4]
