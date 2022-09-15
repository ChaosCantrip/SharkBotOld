from . import errors as DestinyErrors


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
        icon="(Barrier Icon)"
    ),
    Champion(
        name="Overload",
        icon="(Overload Icon)"
    ),
    Champion(
        name="Unstoppable",
        icon="(Unstoppable Icon)"
    )
]


def get(search: str) -> Champion:
    for champion in champions:
        if champion.name == search:
            return champion
    else:
        raise DestinyErrors.ChampionNotFoundError(search)
