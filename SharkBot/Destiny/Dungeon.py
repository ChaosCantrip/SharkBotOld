from typing import TypedDict


class _DungeonData(TypedDict):
    name: str
    destination: str


class Dungeon:

    def __init__(self, name: str, destination: str) -> None:
        self.name = name
        self.destination = destination
