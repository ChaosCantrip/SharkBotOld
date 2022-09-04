class MemberStats:

    def __init__(self, data: dict[str, int]):
        self.coinflipWins: int = data["coinflipWins"] if "coinflipWins" in data else 0
        self.coinflipLosses: int = data["coinflipLosses"] if "coinflipLosses" in data else 0
        self.coinflipMercies: int = data["coinflipMercies"] if "coinflipMercies" in data else 0
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
            "coinflipWins": self.coinflipWins,
            "coinflipLosses": self.coinflipLosses,
            "coinflipMercies": self.coinflipMercies,
            "claims": self.claims,
            "incorrectCounts": self.incorrectCounts,
            "claimedBoxes": self.claimedBoxes,
            "boughtBoxes": self.boughtBoxes,
            "openedBoxes": self.openedBoxes,
            "soldItems": self.soldItems,
            "completedMissions": self.completedMissions,
            "countingBoxes": self.countingBoxes
        }

    @property
    def coinflipwinrate(self) -> float:
        totalCoinflips = self.coinflipWins + self.coinflipLosses
        if totalCoinflips == 0:
            return 0.00
        else:
            return round(self.coinflipWins * 100 / totalCoinflips, 2)

    @property
    def coinflipkda(self) -> str:
        return f"{self.coinflipWins}|{self.coinflipLosses}|{self.coinflipMercies}"
