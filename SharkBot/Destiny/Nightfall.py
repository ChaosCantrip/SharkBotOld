from SharkBot import Destiny
from typing import TypedDict


class _DifficultyData(TypedDict):
    champions: dict[str, int]
    shields: dict[str, int]
