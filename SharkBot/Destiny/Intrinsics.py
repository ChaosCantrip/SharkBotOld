from .Definitions import Definitions
from . import Enums

ROOT_NODE_DEFINITION = Definitions.DestinyPresentationNodeDefinition.get(2214408526)

Intrinsics: dict[str, list[str]] = {breaker.capitalize(): [] for breaker in Enums.BreakerType.__members__.keys()}

for _child_node in ROOT_NODE_DEFINITION["children"]["presentationNodes"]:
    _node_definition = Definitions.DestinyPresentationNodeDefinition.get(_child_node["presentationNodeHash"])
    for _child_collectible in _node_definition["children"]["collectibles"]:
        _collectible_definition = Definitions.DestinyCollectibleDefinition.get(_child_collectible["collectibleHash"])
        _item_definition = Definitions.DestinyInventoryItemDefinition.get(_collectible_definition["itemHash"])
        if (_breaker_type:=_item_definition["breakerType"]) != 0:
            Intrinsics[Enums.BreakerType(_breaker_type).name.capitalize()].append(_item_definition["displayProperties"]["name"])