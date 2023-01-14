from datetime import datetime
from typing import TypedDict, Optional, Union

_EXPIRY_FORMAT = "%d/%m/%Y-%H:%M:%S"

from SharkBot.Errors import Effects as Errors

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
    def expired(self) -> bool:
        if self._charges is not None:
            return self._charges <= 0
        elif self._expiry is not None:
            return self._expiry < datetime.utcnow()
        else:
            raise Errors.InvalidEffectDataError(self.data)

    @property
    def _expiry_data(self) -> Optional[str]:
        if self._expiry is None:
            return None
        else:
            return datetime.strftime(self._expiry, _EXPIRY_FORMAT)

    @property
    def data(self) -> _MemberEffectData:
        return {
            "id": self.id,
            "expiry": self._expiry_data,
            "charges": self._charges
        }


class MemberEffects:

    def __init__(self, member_data: list[_MemberEffectData]):
        self._effects: list[_MemberEffect] = [_MemberEffect(**effect_data) for effect_data in member_data]

    def __contains__(self, item):
        self.effect_is_active(item)

    def remove_expired(self):
        for effect in self._effects:
            if effect.expired:
                self._effects.remove(effect)

    def effect_is_active(self, effect_id: str) -> bool:
        for effect in self._effects:
            if effect.id == effect_id:
                return not effect.expired
        else:
            return False

    @property
    def data(self) -> list[_MemberEffectData]:
        self.remove_expired()
        return [effect.data for effect in self._effects]
