from typing import Self


class ComponentTypeEnum:
    enum_dict: dict[int, Self] = {}
    enum_list: list[Self] = []

    def __init__(self, name: str, enum: int, description: str):
        self.name = name
        self.enum = enum
        self.description = description