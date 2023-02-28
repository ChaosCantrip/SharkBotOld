from . import Manifest

class ManifestLookup:

    def __init__(self, definition_type: str):
        self.definition_type = definition_type

    def get(self, definition_hash: int | str) -> dict:
        return Manifest.get_definition(self.definition_type, definition_hash)

    def get_multiple(self, definition_hashes: list[int | str]) -> dict[str, dict]:
        return Manifest.get_definitions(self.definition_type, definition_hashes)

    def get_all(self) -> dict[str, dict]:
        return Manifest.get_all_definitions(self.definition_type)


class Definitions:
    DestinyPlaceDefinition = ManifestLookup("DestinyPlaceDefinition")
    DestinyActivityDefinition = ManifestLookup("DestinyActivityDefinition")
    DestinyActivityTypeDefinition = ManifestLookup("DestinyActivityTypeDefinition")
    DestinyClassDefinition = ManifestLookup("DestinyClassDefinition")
    DestinyGenderDefinition = ManifestLookup("DestinyGenderDefinition")
    DestinyInventoryBucketDefinition = ManifestLookup("DestinyInventoryBucketDefinition")
    DestinyRaceDefinition = ManifestLookup("DestinyRaceDefinition")
    DestinyTalentGridDefinition = ManifestLookup("DestinyTalentGridDefinition")
    DestinyUnlockDefinition = ManifestLookup("DestinyUnlockDefinition")
    DestinySandboxPerkDefinition = ManifestLookup("DestinySandboxPerkDefinition")
    DestinyStatGroupDefinition = ManifestLookup("DestinyStatGroupDefinition")
    DestinyFactionDefinition = ManifestLookup("DestinyFactionDefinition")
    DestinyVendorGroupDefinition = ManifestLookup("DestinyVendorGroupDefinition")
    DestinyRewardSourceDefinition = ManifestLookup("DestinyRewardSourceDefinition")
    DestinyItemCategoryDefinition = ManifestLookup("DestinyItemCategoryDefinition")
    DestinyDamageTypeDefinition = ManifestLookup("DestinyDamageTypeDefinition")
    DestinyActivityModeDefinition = ManifestLookup("DestinyActivityModeDefinition")
    DestinyMedalTierDefinition = ManifestLookup("DestinyMedalTierDefinition")
    DestinyAchievementDefinition = ManifestLookup("DestinyAchievementDefinition")
    DestinyActivityGraphDefinition = ManifestLookup("DestinyActivityGraphDefinition")
    DestinyBondDefinition = ManifestLookup("DestinyBondDefinition")
    DestinyCollectibleDefinition = ManifestLookup("DestinyCollectibleDefinition")
    DestinyDestinationDefinition = ManifestLookup("DestinyDestinationDefinition")
    DestinyEquipmentSlotDefinition = ManifestLookup("DestinyEquipmentSlotDefinition")
    DestinyEventCardDefinition = ManifestLookup("DestinyEventCardDefinition")
    DestinyStatDefinition = ManifestLookup("DestinyStatDefinition")
    DestinyInventoryItemDefinition = ManifestLookup("DestinyInventoryItemDefinition")
    DestinyItemTierTypeDefinition = ManifestLookup("DestinyItemTierTypeDefinition")
    DestinyLocationDefinition = ManifestLookup("DestinyLocationDefinition")
    DestinyLoreDefinition = ManifestLookup("DestinyLoreDefinition")
    DestinyMaterialRequirementSetDefinition = ManifestLookup("DestinyMaterialRequirementSetDefinition")
    DestinyMetricDefinition = ManifestLookup("DestinyMetricDefinition")
    DestinyObjectiveDefinition = ManifestLookup("DestinyObjectiveDefinition")
    DestinyPlugSetDefinition = ManifestLookup("DestinyPlugSetDefinition")
    DestinyPowerCapDefinition = ManifestLookup("DestinyPowerCapDefinition")
    DestinyPresentationNodeDefinition = ManifestLookup("DestinyPresentationNodeDefinition")
    DestinyProgressionDefinition = ManifestLookup("DestinyProgressionDefinition")
    DestinyProgressionLevelRequirementDefinition = ManifestLookup("DestinyProgressionLevelRequirementDefinition")
    DestinyRecordDefinition = ManifestLookup("DestinyRecordDefinition")
    DestinySackRewardItemListDefinition = ManifestLookup("DestinySackRewardItemListDefinition")
    DestinySandboxPatternDefinition = ManifestLookup("DestinySandboxPatternDefinition")
    DestinySeasonDefinition = ManifestLookup("DestinySeasonDefinition")
    DestinySeasonPassDefinition = ManifestLookup("DestinySeasonPassDefinition")
    DestinySocketCategoryDefinition = ManifestLookup("DestinySocketCategoryDefinition")
    DestinySocketTypeDefinition = ManifestLookup("DestinySocketTypeDefinition")
    DestinyTraitDefinition = ManifestLookup("DestinyTraitDefinition")
    DestinyTraitCategoryDefinition = ManifestLookup("DestinyTraitCategoryDefinition")
    DestinyVendorDefinition = ManifestLookup("DestinyVendorDefinition")
    DestinyMilestoneDefinition = ManifestLookup("DestinyMilestoneDefinition")
    DestinyActivityModifierDefinition = ManifestLookup("DestinyActivityModifierDefinition")
    DestinyReportReasonCategoryDefinition = ManifestLookup("DestinyReportReasonCategoryDefinition")
    DestinyArtifactDefinition = ManifestLookup("DestinyArtifactDefinition")
    DestinyBreakerTypeDefinition = ManifestLookup("DestinyBreakerTypeDefinition")
    DestinyChecklistDefinition = ManifestLookup("DestinyChecklistDefinition")
    DestinyEnergyTypeDefinition = ManifestLookup("DestinyEnergyTypeDefinition")
    DestinyHistoricalStatsDefinition = ManifestLookup("DestinyHistoricalStatsDefinition")
