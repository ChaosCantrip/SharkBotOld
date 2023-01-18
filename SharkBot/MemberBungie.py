from datetime import datetime
from typing import Optional
import aiohttp
import secret
from SharkBot import Errors


class MemberBungie:

    def __init__(self, member):
        self._member = member
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
        self._refresh_token_expires: Optional[datetime] = None

    async def _refresh_token(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(secret.BungieAPI.REFRESH_URL, data=secret.BungieAPI.refresh_headers(self._member.id)) as response:
                if response.ok:
                    return True
                else:
                    return False
