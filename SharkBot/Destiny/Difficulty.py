from SharkBot import Destiny


class Difficulty:

    def __init__(self, champions: dict[str, int], shields: dict[str, int]) -> None:
        self.champions = {Destiny.Champion.get(champion): number for champion, number in champions.items()}
        self.shields = {Destiny.Shield.get(shield): number for shield, number in shields.items()}

    @property
    def champion_types(self) -> list[Destiny.Champion]:
        return list(self.champions.keys())

    @property
    def shield_types(self) -> list[Destiny.Shield]:
        return list(self.shields.keys())

    @property
    def champion_list(self) -> str:
        return "\n".join(f"{champion} x{number}" for champion, number in self.champions.items())

    @property
    def shield_list(self) -> str:
        return "\n".join(f"{shield} x{number}" for shield, number in self.shields.items())

    @property
    def details(self) -> str:
        return f"{self.champion_list}\n{self.shield_list}"
