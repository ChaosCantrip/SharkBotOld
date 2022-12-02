from . import Errors as DestinyErrors


class Champion:
    champions = []

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"

    @classmethod
    def get(cls, search: str):
        for champion in cls.champions:
            if champion.name == search:
                return champion
        else:
            raise DestinyErrors.ChampionNotFoundError(search)


Champion.champions = [
    Champion(
        name="Barrier",
        icon="<:barrier_icon:1021291159949160528>"
    ),
    Champion(
        name="Overload",
        icon="<:overload_icon:1021291162427998238>"
    ),
    Champion(
        name="Unstoppable",
        icon="<:unstoppable_icon:1021291161006125067>"
    )
]
