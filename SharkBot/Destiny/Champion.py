from typing import Self

from . import Errors as DestinyErrors

from SharkBot import Icon


class Champion:
    champions = {}

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def icon(self) -> str:
        return Icon.get(f"{self.name}_icon")

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"

    @classmethod
    def get(cls, search: str) -> Self:
        search = search.lower()
        try:
            return cls.champions[search]
        except KeyError:
            raise DestinyErrors.ChampionNotFoundError(search)


Champion.champions = {
    champion.lower(): Champion(name=champion) for champion in ["Barrier", "Overload", "Unstoppable"]
}
