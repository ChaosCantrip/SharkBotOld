from enum import Enum as _Enum


class GuardianRace(_Enum):
    HUMAN = 0
    AWOKEN = 1
    EXO = 2


class GuardianClass(_Enum):
    TITAN = 0
    HUNTER = 1
    WARLOCK = 2


class BreakerType(_Enum):
    BARRIER = 1
    OVERLOAD = 2
    UNSTOPPABLE = 3


class GuardianStats(_Enum):
    MOBILITY = 2996146975
    RESILIENCE = 392767087
    RECOVERY = 1943323491
    DISCIPLINE = 1735777505
    INTELLECT = 144602215
    STRENGTH = 4244567218


class AmmoType(_Enum):
    PRIMARY = 1
    SPECIAL = 2
    HEAVY = 3


class ComponentType(_Enum):
    Profiles = 100
    VendorReceipts = 101
    ProfileInventories = 102
    ProfileCurrencies = 103
    ProfileProgression = 104
    PlatformSilver = 105
    Characters = 200
    CharacterInventories = 201
    CharacterProgressions = 202
    CharacterRenderData = 203
    CharacterActivities = 204
    CharacterEquipment = 205
    CharacterLoadouts = 206
    ItemInstances = 300
    ItemObjectives = 301
    ItemPerks = 302
    ItemRenderData = 303
    ItemStats = 304
    ItemSockets = 305
    ItemTalentGrids = 306
    ItemCommonData = 307
    ItemPlugStates = 308
    ItemPlugObjectives = 309
    ItemReusablePlugs = 310
    Vendors = 400
    VendorCategories = 401
    VendorSales = 402
    Kiosks = 500
    CurrencyLookups = 600
    PresentationNodes = 700
    Collectibles = 800
    Records = 900
    Transitory = 1000
    Metrics = 1100
    StringVariables = 1200
    Craftables = 1300
    SocialCommendations = 1400
