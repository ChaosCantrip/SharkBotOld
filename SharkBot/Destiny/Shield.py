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
        icon="<:arc_icon:1021291215074889819>"
    ),
    Shield(
        name="Solar",
        icon="<:solar_icon:1021291213430730833>"
    ),
    Shield(
        name="Void",
        icon="<:void_icon:1021291212205981706>"
    )
]


def get(search: str) -> Shield:
    for shield in shields:
        if shield.name == search:
            return shield
    else:
        raise DestinyErrors.ShieldNotFoundError(search)
