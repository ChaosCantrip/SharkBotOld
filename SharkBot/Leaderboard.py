from typing import Callable, Union
import SharkBot

class Leaderboard:

    def __init__(self, name: str, method: Callable[[SharkBot.Member.Member], Union[int, float]]):
        self.name = name
        self.method = method

    def create_current(self) -> dict[str, Union[int, float]]:
        return {str(member.id): self.method(member) for member in SharkBot.Member.members}