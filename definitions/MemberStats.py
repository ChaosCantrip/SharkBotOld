class MemberStats:

    def __init__(self, data: dict[str, int]):
        self._coinflipWins: int = data["coinflipWins"] if "coinflipWins" in data else 0
        self._coinflipLosses: int = data["coinflipLosses"] if "coinflipLosses" in data else 0
        self.coinflipWinRate: float = round(self._coinflipWins / (self._coinflipLosses + self._coinflipWins), 2)
        self.claims: int = data["claims"] if "claims" in data else 0
        self.incorrectCounts: int = data["incorrectCounts"] if "incorrectCounts" in data else 0

    @property
    def data(self) -> dict[str, int]:
        return {
            "coinflipWins": self._coinflipWins,
            "coinflipLosses": self._coinflipLosses,
            "claims": self.claims,
            "incorrectCounts": self.incorrectCounts
        }

    @property
    def coinflipWins(self) -> int:
        return self._coinflipWins

    @coinflipWins.setter
    def coinflipWins(self, value: int) -> None:
        self._coinflipWins = value
        self.coinflipWinRate = round(self._coinflipWins / (self._coinflipLosses + self._coinflipWins), 2)

    @property
    def coinflipLosses(self) -> int:
        return self._coinflipLosses

    @coinflipWins.setter
    def coinflipLosses(self, value: int) -> None:
        self._coinflipLosses = value
        self.coinflipWinRate = round(self._coinflipWins / (self._coinflipLosses + self._coinflipWins), 2)