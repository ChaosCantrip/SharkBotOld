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
        icon="<:arc_icon:1020115323032174602>"
    ),
    Shield(
        name="Solar",
        icon="<:solar_icon:1020115321568366612>"
    ),
    Shield(
        name="Void",
        icon="<:void_icon:1020115319622213662>"
    )
]


def get(search: str) -> Shield:
    for shield in shields:
        if shield.name == search:
            return shield
    else:
        raise DestinyErrors.ShieldNotFoundError(search)
