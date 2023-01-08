import json
from typing import Optional, Self


class MemberDataConverter:
    pass

class _VERSION:

    @classmethod
    def _get_version(cls):
        return int(cls.__name__[-1])

    @classmethod
    def _get_last_version(cls) -> Self:
        return exec(f"_Version{cls._get_version() - 1}")

    @classmethod
    def convert(cls, member_data: dict) -> dict:
        if member_data["data_version"] != cls._get_version() - 1:
            member_data = cls._get_last_version().convert(member_data)
        return cls._convert(member_data)

    @staticmethod
    def _convert(member_data: dict) -> dict:
        return member_data

with open("data/static/members/default_values.json") as infile:
    _LATEST = json.load(infile)["data_version"]
