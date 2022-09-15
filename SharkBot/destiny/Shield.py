from . import Errors as DestinyErrors


class Shield:

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

    @property
    def text(self) -> str:
        return f"{self.icon} {self.name}"


shields = [
    Shield(
        name="Arc",
        icon="(Arc Icon)"
    ),
    Shield(
        name="Solar",
        icon="(Solar Icon)"
    ),
    Shield(
        name="Void",
        icon="(Void Icon)"
    )
]


def get(search: str) -> Shield:
    for shield in shields:
        if shield.name == search:
            return shield
    else:
        raise DestinyErrors.ShieldNotFoundError(search)
