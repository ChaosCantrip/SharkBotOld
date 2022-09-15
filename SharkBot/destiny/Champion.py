from . import Errors as DestinyErrors


class Champion:

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

    @property
    def text(self) -> str:
        return f"{self.icon} {self.name}"


champions = [
    Champion(
        name="Barrier",
        icon="<:barrier_icon:1020115326505074800>"
    ),
    Champion(
        name="Overload",
        icon="<:overload_icon:1020115325397778454>"
    ),
    Champion(
        name="Unstoppable",
        icon="<:unstoppable_icon:1020115324273709058>"
    )
]


def get(search: str) -> Champion:
    for champion in champions:
        if champion.name == search:
            return champion
    else:
        raise DestinyErrors.ChampionNotFoundError(search)
