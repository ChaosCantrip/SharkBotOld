import json
from .MemberDataVersions import *


class MemberDataConverter:

    @staticmethod
    def _get_latest_version() -> VERSION:
        return versions[-1]

    @classmethod
    def convert(cls, member_data: dict) -> tuple[bool, dict]:
        if "data_version" not in member_data:
            member_data["data_version"] = 1
        if member_data["data_version"] == _LATEST:
            return False, member_data
        else:
            return True, cls._get_latest_version().convert(member_data)

with open("data/static/members/default_values.json") as infile:
    _LATEST = json.load(infile)["data_version"]
