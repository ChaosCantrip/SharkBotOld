import datetime
from dataclasses import dataclass
from SharkBot import Utils, Destiny

@dataclass
class WellspringWeapon:
    name: str
    type: str
    ammo: Destiny.AmmoType | str
    energy: Destiny.Shield | str

    def __post_init__(self):
        self.ammo = Destiny.AmmoType.get(self.ammo)
        self.energy = Destiny.Shield.get(self.energy)

    @property
    def icons(self) -> str:
        return f"{self.ammo.icon} {self.energy.icon}"

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

WELLSPRING_DATA = WellspringData(**Utils.JSON.load("data/static/destiny/wellspring_rotation.json"))

class Wellspring:

    @classmethod
    def get_current(cls) -> WellspringDetails:
        return WELLSPRING_DATA.rotation[Destiny.get_day_index(relative_to=WELLSPRING_DATA.rotation_start) % 4]
