
class _CoinflipStats:

    def __init__(self, wins: int = 0, losses: int = 0, mercies: int = 0):
        self.wins = wins
        self.losses = losses
        self.mercies = mercies

    @property
    def winrate(self) -> float:
        total = self.wins + self.losses
        if total == 0:
            return 0.00
        else:
            return round(self.wins * 100 / total, 2)

    @property
    def kda(self) -> str:
        return f"{self.wins}|{self.losses}|{self.mercies}"

    @property
    def data(self) -> dict[str, int]:
        return {
            "wins": self.wins,
            "losses": self.losses,
            "mercies": self.mercies
        }


class MemberStats:

    def __init__(self, data: dict[str, int], coinflips: dict[str, int]):
        self.coinflips = _CoinflipStats(**coinflips)
        self.claims: int = data["claims"] if "claims" in data else 0
        self.incorrectCounts: int = data["incorrectCounts"] if "incorrectCounts" in data else 0
        self.claimedBoxes: int = data["claimedBoxes"] if "claimedBoxes" in data else 0
        self.boughtBoxes: int = data["boughtBoxes"] if "boughtBoxes" in data else 0
        self.openedBoxes: int = data["openedBoxes"] if "openedBoxes" in data else 0
        self.soldItems: int = data["soldItems"] if "soldItems" in data else 0
        self.completedMissions: int = data["completedMissions"] if "completedMissions" in data else 0
        self.countingBoxes: int = data["countingBoxes"] if "countingBoxes" in data else 0

    @property
    def data(self) -> dict[str, int]:
        return {
            "coinflips": self.coinflips.data,
            "claims": self.claims,
            "incorrectCounts": self.incorrectCounts,
            "claimedBoxes": self.claimedBoxes,
            "boughtBoxes": self.boughtBoxes,
            "openedBoxes": self.openedBoxes,
            "soldItems": self.soldItems,
            "completedMissions": self.completedMissions,
            "countingBoxes": self.countingBoxes
        }