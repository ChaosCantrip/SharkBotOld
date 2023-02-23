from typing import Self

from . import Errors as DestinyErrors

from SharkBot import Icon


class Shield:
    shields = {}

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def icon(self) -> str:
        return Icon.get(f"{self.name.lower()}_icon")

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"

    @classmethod
    def get(cls, search: str) -> Self:
        search = search.lower()
        try:
            return cls.shields[search]
        except KeyError:
            raise DestinyErrors.ShieldNotFoundError(search)


Shield.shields = {
    shield.lower(): Shield(name=shield) for shield in ["Arc", "Solar", "Void", "Stasis", "Kinetic"]
}
