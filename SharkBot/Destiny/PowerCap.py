from enum import IntEnum as _IntEnum

class _Enum(_IntEnum):

    @classmethod
    def items(cls):
        return [
            (" ".join(name.split("_")).title(), int(value))
            for name, value in cls.__members__.items()
        ]

class Gear(_Enum):
    POWER_FLOOR = 1600
    SOFT_CAP = 1750
    POWER_CAP = 1800
    HARD_CAP = POWER_CAP + 10

class Activity(_Enum):
    LEGEND = Gear.HARD_CAP + 20
    MASTER = Gear.HARD_CAP + 30
    GRANDMASTER = MASTER

class MaxEffectivePower(_Enum):
    LEGEND = Activity.LEGEND - 15
    MASTER = Activity.MASTER - 20
    GRANDMASTER = Activity.GRANDMASTER - 25