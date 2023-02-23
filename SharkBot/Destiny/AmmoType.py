from typing import Self

from . import Errors as DestinyErrors

from SharkBot import Icon


class AmmoType:
    ammo_types = {}

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
            return cls.ammo_types[search]
        except KeyError:
            raise DestinyErrors.AmmoTypeNotFoundError(search)


AmmoType.ammo_types = {
    ammo.lower(): AmmoType(name=ammo) for ammo in ["Primary", "Special", "Heavy"]
}
