
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


class _BoxesStats:

    def __init__(self, claimed: int = 0, bought: int = 0, opened: int = 0, counting: int = 0):
        self.claimed = claimed
        self.bought = bought
        self.opened = opened
        self.counting = counting

    @property
    def data(self) -> dict[str, int]:
        return {
            "claimed": self.claimed,
            "bought": self.bought,
            "opened": self.opened,
            "counting": self.counting
        }


class MemberStats:

    def __init__(self, coinflips: dict[str, int], boxes: dict[str, int], completed_missions: int = 0, sold_items: int = 0, claims: int = 0, incorrect_counts: int = 0):
        self.coinflips = _CoinflipStats(**coinflips)
        self.boxes = _BoxesStats(**boxes)
        self.claims = claims
        self.incorrect_counts = incorrect_counts
        self.sold_items = sold_items
        self.completed_missions = completed_missions

    @property
    def data(self) -> dict[str, int]:
        return {
            "coinflips": self.coinflips.data,
            "boxes": self.boxes.data,
            "claims": self.claims,
            "incorrect_counts": self.incorrect_counts,
            "sold_items": self.sold_items,
            "completed_missions": self.completed_missions
        }