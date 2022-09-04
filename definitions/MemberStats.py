class MemberStats:

    def __init__(self, data: dict[str, int]):
        self.coinflipWins: int = data["coinflipWins"] if "coinflipWins" in data else 0
        self.coinflipLosses: int = data["coinflipLosses"] if "coinflipLosses" in data else 0
        self.coinflipMercies: int = data["coinflipMercies"] if "coinflipMercies" in data else 0
        self.claims: int = data["claims"] if "claims" in data else 0
        self.incorrectCounts: int = data["incorrectCounts"] if "incorrectCounts" in data else 0

    @property
    def data(self) -> dict[str, int]:
        return {
            "coinflipWins": self.coinflipWins,
            "coinflipLosses": self.coinflipLosses,
            "coinflipMercies": self.coinflipMercies,
            "claims": self.claims,
            "incorrectCounts": self.incorrectCounts
        }

    @property
    def coinflipwinrate(self) -> float:
        totalCoinflips = self.coinflipWins + self.coinflipLosses
        if totalCoinflips == 0:
            return 0.00
        else:
            return round(self.coinflipWins / totalCoinflips, 2)

    @property
    def coinflipkda(self) -> str:
        return f"{self.coinflipWins}|{self.coinflipLosses}|{self.coinflipMercies}"
