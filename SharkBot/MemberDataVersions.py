from typing import Self

class VERSION:

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


class Version1(VERSION):

    @staticmethod
    def _convert(member_data: dict) -> dict:
        return member_data

versions = [
    Version1
]