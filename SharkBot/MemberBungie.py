import json
from datetime import datetime
from typing import Optional, Union
import aiohttp
import secret

import SharkBot


class _CraftablesResponse:

    def __init__(self, weapon_name: str, record_data: dict[str, Union[int, bool]]):
        self.weapon_name = weapon_name
        self.progress: int = record_data["progress"]
        self.quota: int = record_data["completionValue"]
        self.complete: bool = record_data["complete"]


class MemberBungie:

    def __init__(self, member, token: Optional[str] = None, token_expires: Optional[int] = None,
                 refresh_token_expires: Optional[int] = None, destiny_membership_id: Optional[str] = None,
                 destiny_membership_type: Optional[int] = None):
        self._member: SharkBot.Member.Member = member
        self._token = token
        self._token_expires = token_expires
        self._refresh_token_expires = refresh_token_expires
        self._destiny_membership_id = destiny_membership_id
        self._destiny_membership_type = destiny_membership_type

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
            raise SharkBot.Errors.BungieAPI.RefreshFailedError(self._member.id)

        doc_ref = SharkBot.Handlers.firestoreHandler.db.collection(u"bungieauth").document(str(self._member.id))
        doc = doc_ref.get()

        if not doc.exists:
            raise SharkBot.Errors.BungieAPI.SetupNeededError(self._member.id)

        data = doc.to_dict()
        self._token = data["access_token"]
        self._token_expires = datetime.utcnow().timestamp() + data["expires_in"]
        self._refresh_token_expires = data["refresh_expires_in"] + data["refreshed_at"]
        self._destiny_membership_id = data["destiny_membership_id"]
        self._destiny_membership_type = data["destiny_membership_type"]
        self._member.write_data()
        return self._token

    async def get_craftables_data(self) -> dict[str, list[_CraftablesResponse]]:
        token = await self._get_token()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://www.bungie.net/Platform/Destiny2/{self._destiny_membership_type}/Profile/{self._destiny_membership_id}?components=900",
                    headers=secret.BungieAPI.bungie_headers(token)
            ) as response:
                if not response.ok:
                    raise SharkBot.Errors.BungieAPI.InternalServerError(await response.json())
                else:
                    data = await response.json()
                    records = data["Response"]["profileRecords"]["data"]["records"]
                    output = {}
                    for weapon_type, weapon_records in _crafting_records.items():
                        weapon_data = []
                        for weapon_name, record_hash in weapon_records.items():
                            weapon_data.append(_CraftablesResponse(
                                weapon_name=weapon_name,
                                record_data=records[record_hash]["objectives"][0]
                            ))
                        output[weapon_type] = weapon_data
        return output

    @property
    def data(self) -> dict:
        return {
            "token": self._token,
            "token_expires": self._token_expires,
            "refresh_token_expires": self._refresh_token_expires,
            "destiny_membership_id": self._destiny_membership_id,
            "destiny_membership_type": self._destiny_membership_type
        }


with open("data/static/bungie/definitions/CraftingRecords.json", "r") as infile:
    _crafting_records: dict[str, dict[str, str]] = json.load(infile)
