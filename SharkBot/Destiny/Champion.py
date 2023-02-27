from typing import Self

from . import Errors as DestinyErrors

from SharkBot import Icon
from SharkBot.Destiny.Manifest import get_definitions_file


class Champion:
    champions = {}
    champion_hashes: dict[str, list[Self]] = {}

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
            return cls.champions[search]
        except KeyError:
            raise DestinyErrors.ChampionNotFoundError(search)


Champion.champions = {
    champion.lower(): Champion(name=champion) for champion in ["Barrier", "Overload", "Unstoppable"]
}

for modifier_hash, modifier_definition in get_definitions_file("DestinyActivityModifierDefinition").items():
    if modifier_definition["displayProperties"]["name"] == "Champion Foes":
        champion_types = []
        for champion_type, champion in Champion.champions.items():
            if champion_type.capitalize() in modifier_definition["displayProperties"]["description"]:
                champion_types.append(champion)
        Champion.champion_hashes[modifier_hash] = champion_types
