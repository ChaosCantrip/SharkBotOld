from . import Manifest

class ManifestDefinitionType:

    def __init__(self, definition_type: str):
        self.definition_type = definition_type

    def get(self, definition_hash: int | str) -> dict:
        return Manifest.get_definition(self.definition_type, definition_hash)

    def get_multiple(self, definition_hashes: list[int | str]) -> dict[str, dict]:
        return Manifest.get_definitions(self.definition_type, definition_hashes)

    def get_all(self) -> dict[str, dict]:
        return Manifest.get_all_definitions(self.definition_type)


class Definitions:
    DestinyPlaceDefinition = ManifestDefinitionType("DestinyPlaceDefinition")
    DestinyActivityDefinition = ManifestDefinitionType("DestinyActivityDefinition")
    DestinyActivityTypeDefinition = ManifestDefinitionType("DestinyActivityTypeDefinition")
    DestinyClassDefinition = ManifestDefinitionType("DestinyClassDefinition")
    DestinyGenderDefinition = ManifestDefinitionType("DestinyGenderDefinition")
    DestinyInventoryBucketDefinition = ManifestDefinitionType("DestinyInventoryBucketDefinition")
    DestinyRaceDefinition = ManifestDefinitionType("DestinyRaceDefinition")
    DestinyTalentGridDefinition = ManifestDefinitionType("DestinyTalentGridDefinition")
    DestinyUnlockDefinition = ManifestDefinitionType("DestinyUnlockDefinition")
    DestinySandboxPerkDefinition = ManifestDefinitionType("DestinySandboxPerkDefinition")
    DestinyStatGroupDefinition = ManifestDefinitionType("DestinyStatGroupDefinition")
    DestinyFactionDefinition = ManifestDefinitionType("DestinyFactionDefinition")
    DestinyVendorGroupDefinition = ManifestDefinitionType("DestinyVendorGroupDefinition")
    DestinyRewardSourceDefinition = ManifestDefinitionType("DestinyRewardSourceDefinition")
    DestinyItemCategoryDefinition = ManifestDefinitionType("DestinyItemCategoryDefinition")
    DestinyDamageTypeDefinition = ManifestDefinitionType("DestinyDamageTypeDefinition")
    DestinyActivityModeDefinition = ManifestDefinitionType("DestinyActivityModeDefinition")
    DestinyMedalTierDefinition = ManifestDefinitionType("DestinyMedalTierDefinition")
    DestinyAchievementDefinition = ManifestDefinitionType("DestinyAchievementDefinition")
    DestinyActivityGraphDefinition = ManifestDefinitionType("DestinyActivityGraphDefinition")
    DestinyBondDefinition = ManifestDefinitionType("DestinyBondDefinition")
    DestinyCollectibleDefinition = ManifestDefinitionType("DestinyCollectibleDefinition")
    DestinyDestinationDefinition = ManifestDefinitionType("DestinyDestinationDefinition")
    DestinyEquipmentSlotDefinition = ManifestDefinitionType("DestinyEquipmentSlotDefinition")
    DestinyEventCardDefinition = ManifestDefinitionType("DestinyEventCardDefinition")
    DestinyStatDefinition = ManifestDefinitionType("DestinyStatDefinition")
    DestinyInventoryItemDefinition = ManifestDefinitionType("DestinyInventoryItemDefinition")
    DestinyItemTierTypeDefinition = ManifestDefinitionType("DestinyItemTierTypeDefinition")
    DestinyLocationDefinition = ManifestDefinitionType("DestinyLocationDefinition")
    DestinyLoreDefinition = ManifestDefinitionType("DestinyLoreDefinition")
    DestinyMaterialRequirementSetDefinition = ManifestDefinitionType("DestinyMaterialRequirementSetDefinition")
    DestinyMetricDefinition = ManifestDefinitionType("DestinyMetricDefinition")
    DestinyObjectiveDefinition = ManifestDefinitionType("DestinyObjectiveDefinition")
    DestinyPlugSetDefinition = ManifestDefinitionType("DestinyPlugSetDefinition")
    DestinyPowerCapDefinition = ManifestDefinitionType("DestinyPowerCapDefinition")
    DestinyPresentationNodeDefinition = ManifestDefinitionType("DestinyPresentationNodeDefinition")
    DestinyProgressionDefinition = ManifestDefinitionType("DestinyProgressionDefinition")
    DestinyProgressionLevelRequirementDefinition = ManifestDefinitionType("DestinyProgressionLevelRequirementDefinition")
    DestinyRecordDefinition = ManifestDefinitionType("DestinyRecordDefinition")
    DestinySackRewardItemListDefinition = ManifestDefinitionType("DestinySackRewardItemListDefinition")
    DestinySandboxPatternDefinition = ManifestDefinitionType("DestinySandboxPatternDefinition")
    DestinySeasonDefinition = ManifestDefinitionType("DestinySeasonDefinition")
    DestinySeasonPassDefinition = ManifestDefinitionType("DestinySeasonPassDefinition")
    DestinySocketCategoryDefinition = ManifestDefinitionType("DestinySocketCategoryDefinition")
    DestinySocketTypeDefinition = ManifestDefinitionType("DestinySocketTypeDefinition")
    DestinyTraitDefinition = ManifestDefinitionType("DestinyTraitDefinition")
    DestinyTraitCategoryDefinition = ManifestDefinitionType("DestinyTraitCategoryDefinition")
    DestinyVendorDefinition = ManifestDefinitionType("DestinyVendorDefinition")
    DestinyMilestoneDefinition = ManifestDefinitionType("DestinyMilestoneDefinition")
    DestinyActivityModifierDefinition = ManifestDefinitionType("DestinyActivityModifierDefinition")
    DestinyReportReasonCategoryDefinition = ManifestDefinitionType("DestinyReportReasonCategoryDefinition")
    DestinyArtifactDefinition = ManifestDefinitionType("DestinyArtifactDefinition")
    DestinyBreakerTypeDefinition = ManifestDefinitionType("DestinyBreakerTypeDefinition")
    DestinyChecklistDefinition = ManifestDefinitionType("DestinyChecklistDefinition")
    DestinyEnergyTypeDefinition = ManifestDefinitionType("DestinyEnergyTypeDefinition")
    DestinyHistoricalStatsDefinition = ManifestDefinitionType("DestinyHistoricalStatsDefinition")
