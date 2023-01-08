import json


class MemberDataConverter:
    pass

with open("data/static/members/default_values.json") as infile:
    _LATEST = json.load(infile)["data_version"]
