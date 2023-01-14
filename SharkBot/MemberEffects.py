from datetime import datetime
from typing import TypedDict, Optional


_EXPIRY_FORMAT = "%d/%m/%Y-%H:%M:%S"


class _MemberEffectData(TypedDict):
    id: str
    expiry: Optional[str]
    charges: Optional[int]


class _MemberEffect:

    def __init__(self, effect_id: str, expiry: Optional[str] = None, charges: Optional[int] = None):
        if expiry is not None:
            expiry = datetime.strptime(expiry, _EXPIRY_FORMAT)
        self.id = effect_id
        self._expiry = expiry
        self._charges = charges

    @property
    def expiry(self) -> Optional[datetime]:
        return self._expiry

    @expiry.setter
    def expiry(self, value: datetime):
        self._expiry = value

    @property
    def charges(self) -> Optional[int]:
        return self._charges

    @charges.setter
    def charges(self, value: int):
        self._charges = value

    @property
    def _expiry_data(self) -> Optional[str]:
        if self._expiry is None:
            return None
        else:
            return datetime.strftime(self._expiry, _EXPIRY_FORMAT)


class MemberEffects:
    pass
