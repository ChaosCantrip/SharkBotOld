from datetime import datetime
from typing import Optional


class MemberBungie:

    def __init__(self, member):
        self._member = member
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
        self._refresh_token_expires: Optional[datetime] = None
