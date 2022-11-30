class XP:

    def __init__(self, xp: int):
        self.xp = xp


xp_track = {
    0: 1,
    10: 2,
    25: 3,
    45: 4,
    70: 5,
    100: 6,
    140: 7,
    190: 8,
    250: 9,
    320: 10,
    400: 11,
    490: 12
}

max_xp_in_track = max(xp_track)
