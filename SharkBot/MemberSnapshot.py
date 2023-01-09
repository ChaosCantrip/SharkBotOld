import SharkBot

_SNAPSHOTS_DIRECTORY = "data/live/snapshots/members"

class MemberSnapshot:

    def __init__(self, member):
        self.member: SharkBot.Member.Member = member
        self.path: str = f"{_SNAPSHOTS_DIRECTORY}/{member.id}.json"

SharkBot.Utils.FileChecker.directory(_SNAPSHOTS_DIRECTORY)