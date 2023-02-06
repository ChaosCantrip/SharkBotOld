class MemberSettings:

    def __init__(self, delete_incorrect_counts: bool = False, short_buy_cycle: bool = False):
        self.delete_incorrect_counts = delete_incorrect_counts
        self.short_buy_cycle = short_buy_cycle

    @property
    def data(self) -> dict[str, bool]:
        return {
            "delete_incorrect_counts": self.delete_incorrect_counts,
            "short_buy_cycle": self.short_buy_cycle
        }