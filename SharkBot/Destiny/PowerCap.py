class Gear:
    POWER_FLOOR = 1600
    SOFT_CAP = 1750
    POWER_CAP = 1800
    HARD_CAP = POWER_CAP + 10

class Activity:
    LEGEND = Gear.HARD_CAP + 20
    MASTER = Gear.HARD_CAP + 30
    GRANDMASTER = MASTER

class MaxEffectivePower:
    LEGEND = Activity.LEGEND - 15
    MASTER = Activity.MASTER - 20
    GRANDMASTER = Activity.GRANDMASTER - 25
