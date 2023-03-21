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

class GuardianStats(_Enum):
    MOBILITY = 2996146975
    RESILIENCE = 392767087
    RECOVERY = 1943323491
    DISCIPLINE = 1735777505
    INTELLECT = 144602215
    STRENGTH = 4244567218