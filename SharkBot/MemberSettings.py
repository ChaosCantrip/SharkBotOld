class MemberSettings:

    def __init__(self, delete_incorrect_counts: bool = False):
        self.delete_incorrect_counts = delete_incorrect_counts

    @property
    def data(self) -> dict[str, bool]:
        return {
            "delete_incorrect_counts": self.delete_incorrect_counts
        }