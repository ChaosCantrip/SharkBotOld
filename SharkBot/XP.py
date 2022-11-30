class XP:

    def __init__(self, xp: int):
        self.xp = xp
        self.level = xp_to_level(xp)


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


def xp_to_level(xp: int) -> int:
    if xp > max_xp_in_track:
        return 12 + int((xp - max_xp_in_track) / 100)
    else:
        for x, l in xp_track.items():
            if xp < x:
                return l - 1
