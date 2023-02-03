import json
from typing import Self

from . import Errors


class ComponentTypeEnum:
    enum_dict: dict[int, Self] = {}
    enum_list: list[Self] = []

    def __init__(self, name: str, enum: int, description: str):
        self.name = name
        self.enum = enum
        self.description = description

    @classmethod
    def load(cls) -> None:
        with open("data/static/bungie/definitions/ComponentTypeEnum.json", "r") as infile:
            data: list[dict[str, str | int]] = json.load(infile)
        cls.enum_list = [cls(**d) for d in data]
        cls.enum_dict = {e.enum: e for e in cls.enum_list}

    @classmethod
    def get(cls, search: int) -> Self:
        try:
            return cls.enum_dict[search]
        except KeyError:
            raise Errors.ComponentTypeEnumNotFoundError(search)

ComponentTypeEnum.load()