from typing import Self, Optional

from . import Errors as DestinyErrors

from SharkBot import Icon
from SharkBot.Destiny.Manifest import get_all_definitions


class Champion:
    champions = {}
    champion_hashes: dict[str, list[Self]] = {}

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f"Champion[{self.name}]"

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

    @classmethod
    def from_modifier(cls, _modifier_hash: str | int) -> Optional[list[Self]]:
        try:
            return cls.champion_hashes[str(_modifier_hash)]
        except KeyError:
            return None

    @classmethod
    def from_modifiers(cls, _modifier_hashes: list[str | int]) -> list[Self]:
        _champions = []
        for _modifier_hash in _modifier_hashes:
            _modifier_champions = cls.from_modifier(_modifier_hash)
            if _modifier_champions is not None:
                _champions.extend(_modifier_champions)
        return list(set(_champions))


Champion.champions = {
    champion.lower(): Champion(name=champion) for champion in ["Barrier", "Overload", "Unstoppable"]
}

for modifier_hash, modifier_definition in get_all_definitions("DestinyActivityModifierDefinition").items():
    if modifier_definition["displayProperties"]["name"] == "Champion Foes":
        champion_types = []
        for champion_type, champion in Champion.champions.items():
            if champion_type.capitalize() in modifier_definition["displayProperties"]["description"]:
                champion_types.append(champion)
        Champion.champion_hashes[modifier_hash] = champion_types
