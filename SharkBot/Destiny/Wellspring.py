from dataclasses import dataclass

@dataclass(frozen=True)
class WellspringWeapon:
    name: str
    type: str

@dataclass(frozen=True)
class WellspringDetails:
    mode: str
    boss: str
    weapon: WellspringWeapon

class Wellspring:
    pass