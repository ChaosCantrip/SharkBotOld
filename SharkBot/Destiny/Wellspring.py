from dataclasses import dataclass

@dataclass(frozen=True)
class WellspringWeapon:
    name: str
    type: str

class Wellspring:
    pass