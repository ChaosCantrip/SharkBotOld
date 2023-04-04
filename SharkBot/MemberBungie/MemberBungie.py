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
        self.seals = Seals(self._member)
        self.season_levels = SeasonLevels(self._member)
        self.engram_tracker = EngramTracker(self._member)
        self.power_level = PowerLevel(self._member)
        self.catalysts = Catalysts(self._member)
        self.pinnacles = Pinnacles(self._member)
        self.stats = Stats(self._member)
        self.guardian_ranks = GuardianRanks(self._member)

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
            async with session.post(
                    secret.BungieAPI.REFRESH_URL + f"?member_id={self._member.id}",
                    headers=secret.BungieAPI.refresh_headers()
            ) as response:
                if response.ok:
                    bungie_logger.info(f"{self._member.log_repr} - Token Refresh Successful")
                    return True
                else:
                    bungie_logger.error(f"{self._member.log_repr} - Token Refresh Unsuccessful")
                    raise SharkBot.Errors.BungieAPI.TokenRefreshFailedError(self._member, response, await response.text())

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
        self.seals.wipe_cache()
        self.season_levels.wipe_cache()
        self.engram_tracker.wipe_cache()
        self.power_level.wipe_cache()
        self.catalysts.wipe_cache()
        self.pinnacles.wipe_cache()
        self.stats.wipe_cache()
        self.guardian_ranks.wipe_cache()

    async def get_endpoint_data(self, endpoint: str, headers: dict = None, retry: bool = True) -> dict:
        token = await self._get_token()
        _headers = secret.BungieAPI.bungie_headers(token)
        if headers is not None:
            _headers.update(headers)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    endpoint,
                    headers=_headers
            ) as response:
                if not response.ok:
                    bungie_logger.error(f"{self._member.log_repr} - Endpoint Unsuccessful - Response {response.status} [{endpoint}]")
                    if response.status == 401 and retry:
                        self._token = None
                        return await self.get_endpoint_data(endpoint, retry=False)
                    raise SharkBot.Errors.BungieAPI.InternalServerError(response.status, response.reason)
                else:
                    bungie_logger.info(f"{self._member.log_repr} - Endpoint Successful - Response {response.status} [{endpoint}]")
                    data = await response.json()
                    return data


    async def get_profile_data(self, *components: int, retry: bool = True) -> dict[str, dict]:
        _components_string = ",".join(str(component) for component in components)
        return await self.get_endpoint_data(
            f"https://www.bungie.net/Platform/Destiny2/{self._destiny_membership_type}/Profile/{self._destiny_membership_id}?components={_components_string}"
        )

    async def get_profile_response(self, *components: int) -> dict[str, dict]:
        data = await self.get_profile_data(*components)
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
