from typing import Self, Optional

from . import Errors as DestinyErrors

from SharkBot import Icon
from SharkBot.Destiny.Manifest import get_definitions_file


class Shield:
    shields: dict[str, Self] = {}
    shield_hashes: dict[str, list[Self]] = {}

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f"Shield[{self.name}]"

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

    @classmethod
    def from_modifier(cls, _modifier_hash: str | int) -> Optional[list[Self]]:
        try:
            return cls.shield_hashes[str(_modifier_hash)]
        except KeyError:
            return None

    @classmethod
    def from_modifiers(cls, _modifier_hashes: list[str | int]) -> list[Self]:
        _shields = []
        for _modifier_hash in _modifier_hashes:
            _modifier_shields = cls.from_modifier(_modifier_hash)
            if _modifier_shields is not None:
                _shields.extend(_modifier_shields)
        return list(set(_shields))


Shield.shields = {
    shield.lower(): Shield(name=shield) for shield in ["Arc", "Solar", "Void", "Stasis", "Kinetic"]
}


for modifier_hash, modifier_definition in get_definitions_file("DestinyActivityModifierDefinition").items():
    if modifier_definition["displayProperties"]["name"] == "Shielded Foes":
        shield_types = []
        for shield_type, shield in Shield.shields.items():
            if shield_type.capitalize() in modifier_definition["displayProperties"]["description"]:
                shield_types.append(shield)
        Shield.shield_hashes[modifier_hash] = shield_types