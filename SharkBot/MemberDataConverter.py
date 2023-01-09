import json
from typing import Self

class _VERSION:

    @classmethod
    def _get_version(cls) -> int:
        return int(cls.__name__[-1])

    @classmethod
    def _get_last_version(cls) -> Self:
        return versions[cls._get_version() - 2]

    @classmethod
    def convert(cls, member_data: dict) -> dict:
        if member_data["data_version"] != cls._get_version() - 1:
            member_data = cls._get_last_version().convert(member_data)
        member_data["data_version"] = cls._get_version()
        return cls._convert(member_data)

    @staticmethod
    def _convert(member_data: dict) -> dict:
        return member_data


class _Version1(_VERSION):

    @staticmethod
    def _convert(member_data: dict) -> dict:
        return member_data

versions = [
    _Version1
]


class MemberDataConverter:

    @staticmethod
    def _get_latest_version() -> _VERSION:
        return versions[-1]

    @classmethod
    def convert(cls, member_data: dict) -> dict:
        if "data_version" not in member_data:
            member_data["data_version"] = 1
        if member_data["data_version"] == _LATEST:
            return member_data
        else:
            return cls._get_latest_version().convert(member_data)

with open("data/static/members/default_values.json") as infile:
    _LATEST = json.load(infile)["data_version"]
