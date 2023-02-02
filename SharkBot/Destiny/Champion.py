from . import Errors as DestinyErrors

from SharkBot import Icon


class Champion:
    champions = []

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self._icon = icon

    @property
    def icon(self) -> str:
        return Icon.get(self._icon)

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
        icon="barrier_icon"
    ),
    Champion(
        name="Overload",
        icon="overload_icon"
    ),
    Champion(
        name="Unstoppable",
        icon="unstoppable_icon"
    )
]
