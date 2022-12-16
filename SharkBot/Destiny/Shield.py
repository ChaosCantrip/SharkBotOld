from . import Errors as DestinyErrors


class Shield:
    shields = []

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

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
        icon="<:arc_icon:1021291215074889819>"
    ),
    Shield(
        name="Solar",
        icon="<:solar_icon:1021291213430730833>"
    ),
    Shield(
        name="Void",
        icon="<:void_icon:1021291212205981706>"
    ),
    Shield(
        name="Stasis",
        icon="<:stasis_icon:1021291210566029413>"
    )
]
