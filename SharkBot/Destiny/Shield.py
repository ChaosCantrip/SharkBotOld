from . import Errors as DestinyErrors

from SharkBot import Icon


class Shield:
    shields = []

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
        for shield in cls.shields:
            if shield.name == search:
                return shield
        else:
            raise DestinyErrors.ShieldNotFoundError(search)


Shield.shields = [
    Shield(
        name="Arc",
        icon="arc_icon"
    ),
    Shield(
        name="Solar",
        icon="solar_icon"
    ),
    Shield(
        name="Void",
        icon="void_icon"
    ),
    Shield(
        name="Stasis",
        icon="stasis_icon"
    )
]
