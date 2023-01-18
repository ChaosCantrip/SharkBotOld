from datetime import datetime
from typing import Optional
import aiohttp
import secret
from SharkBot import Errors, Handlers


class MemberBungie:

    def __init__(self, member):
        self._member = member
        self._token: Optional[str] = None
        self._token_expires: Optional[int] = None
        self._refresh_token_expires: Optional[int] = None

    async def _refresh_token(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(secret.BungieAPI.REFRESH_URL, data=secret.BungieAPI.refresh_headers(self._member.id)) as response:
                if response.ok:
                    return True
                else:
                    return False

    def _need_refresh(self) -> bool:
        if self._token_expires is None:
            return True
        else:
            return self._token_expires < datetime.utcnow().timestamp()

    async def _get_token(self):
        if self._token is not None:
            if not self._need_refresh():
                return self._token

        if not await self._refresh_token():
            raise Errors.BungieAPI.RefreshFailedError(self._member.id)

        doc_ref = Handlers.firestoreHandler.db.collection(u"bungieauth").document(str(self._member.id))
        doc = doc_ref.get()

        if not doc.exists:
            raise Errors.BungieAPI.SetupNeededError(self._member.id)

        data = doc.to_dict()
        self._token = data["access_token"]
        self._token_expires = datetime.utcnow().timestamp() + data["expires_in"]
        self._refresh_token_expires = data["refresh_expires_in"] + data["refreshed_at"]
        return self._token
