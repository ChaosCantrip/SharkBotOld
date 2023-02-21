import logging
from datetime import datetime, timedelta
from typing import Optional

import aiohttp

import secret
from .BungieData import *

bungie_logger = logging.getLogger("bungie")

import SharkBot

class _CacheFolders:
    CORE = "data/live/bungie/cache"
    CRAFTABLES = CORE + "/craftables"
    WEAPON_LEVELS = CORE + "/weapon_levels"
    CURRENCY = CORE + "/currencies"
    LIST = [CRAFTABLES, WEAPON_LEVELS, CURRENCY]

SharkBot.Utils.FileChecker.directory(_CacheFolders.CRAFTABLES)
SharkBot.Utils.FileChecker.directory(_CacheFolders.WEAPON_LEVELS)
SharkBot.Utils.FileChecker.directory(_CacheFolders.CURRENCY)


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
        self.craftables = Craftables(self._member)
        self.monument = Monument(self._member)
        self.currencies = Currencies(self._member)
        self.weapon_levels = WeaponLevels(self._member)
        self.bounty_prep = BountyPrep(self._member)
        self.conqueror = Conqueror(self._member)

    def delete_credentials(self) -> bool:
        self.wipe_all_cache()
        self._token = None
        self._token_expires = None
        self._refresh_token_expires = None
        self._destiny_membership_id = None
        self._destiny_membership_type = None

        db = SharkBot.Handlers.firestoreHandler.db
        doc_ref = db.collection(u"bungieauth").document(str(self._member.id))
        doc = doc_ref.get()

        if not doc.exists:
            return False
        else:
            doc_ref.delete()
            return True

    @property
    def refresh_token_expiring(self) -> bool:
        if self._refresh_token_expires is None:
            return False
        else:
            return self._refresh_token_expires < (datetime.utcnow() + timedelta(weeks=1)).timestamp()

    async def soft_refresh(self):
        try:
            await self._refresh_token()
        except Exception as e:
            pass

    async def _refresh_token(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(secret.BungieAPI.REFRESH_URL, data=secret.BungieAPI.refresh_headers(self._member.id)) as response:
                if response.ok:
                    bungie_logger.info(f"{self._member.log_repr} - Token Refresh Successful")
                    return True
                else:
                    bungie_logger.error(f"{self._member.log_repr} - Token Refresh Unsuccessful")
                    return False

    def _need_refresh(self) -> bool:
        if self._token_expires is None:
            return True
        else:
            return self._token_expires < datetime.utcnow().timestamp() - 60

    async def _get_token(self):
        if self._token is not None:
            if not self._need_refresh():
                return self._token

        doc_ref = SharkBot.Handlers.firestoreHandler.db.collection(u"bungieauth").document(str(self._member.id))
        doc = doc_ref.get()

        if not doc.exists:
            raise SharkBot.Errors.BungieAPI.SetupNeededError(self._member.id)

        if not await self._refresh_token():
            raise SharkBot.Errors.BungieAPI.InternalServerError(self._member.id)

        doc = doc_ref.get()

        data = doc.to_dict()
        self._token = data["access_token"]
        self._token_expires = datetime.utcnow().timestamp() + data["expires_in"]
        self._refresh_token_expires = data["refresh_expires_in"] + data["refreshed_at"]
        self._destiny_membership_id = data["destiny_membership_id"]
        self._destiny_membership_type = data["destiny_membership_type"]
        bungie_logger.info(f"{self._member.log_repr} - Retrieved Token")
        self._member.write_data()
        return self._token

    def wipe_all_cache(self):
        self.craftables.wipe_cache()
        self.monument.wipe_cache()
        self.currencies.wipe_cache()
        self.weapon_levels.wipe_cache()
        self.bounty_prep.wipe_cache()
        self.conqueror.wipe_cache()

    async def get_endpoint_data(self, *components: int) -> dict[str, dict]:
        _components_string = ",".join(str(component) for component in components)
        token = await self._get_token()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://www.bungie.net/Platform/Destiny2/{self._destiny_membership_type}/Profile/{self._destiny_membership_id}?components={_components_string}",
                    headers=secret.BungieAPI.bungie_headers(token)
            ) as response:
                if not response.ok:
                    bungie_logger.error(f"{self._member.log_repr} - Endpoint Unsuccessful - Response {response.status} [{_components_string}]")
                    self._token = None
                    raise SharkBot.Errors.BungieAPI.InternalServerError
                else:
                    bungie_logger.info(f"{self._member.log_repr} - Endpoint Successful - Response {response.status} [{_components_string}]")
                    data = await response.json()
                    return data

    async def get_profile_response(self, *components: int) -> dict[str, dict]:
        data = await self.get_endpoint_data(*components)
        return data["Response"]

    @property
    def data(self) -> dict:
        return {
            "token": self._token,
            "token_expires": self._token_expires,
            "refresh_token_expires": self._refresh_token_expires,
            "destiny_membership_id": self._destiny_membership_id,
            "destiny_membership_type": self._destiny_membership_type
        }
