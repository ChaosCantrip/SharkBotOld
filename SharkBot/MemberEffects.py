from typing import TypedDict, Optional


class _MemberEffectData(TypedDict):
    id: str
    expiry: Optional[str]
    charges: Optional[int]

class _MemberEffect:
    pass

class MemberEffects:
    pass
