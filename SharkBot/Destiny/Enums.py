from enum import Enum as _Enum

class GuardianRace(_Enum):
    HUMAN = 0
    AWOKEN = 1
    EXO = 2

class GuardianClass(_Enum):
    TITAN = 0
    HUNTER = 1
    WARLOCK = 2

class BreakerType(_Enum):
    BARRIER = 1
    OVERLOAD = 2
    UNSTOPPABLE = 3