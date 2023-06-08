
from ......rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
AssetChanged = make_struct("AssetChanged", [("asset_id", "iroha_data_model.asset.Id"), ("amount", "iroha_data_model.asset.AssetValue")])

AssetDefinitionEvent = make_enum("AssetDefinitionEvent", [("Created", get_class("iroha_data_model.asset.AssetDefinition")), ("MintabilityChanged", get_class("iroha_data_model.asset.DefinitionId")), ("OwnerChanged", get_class("iroha_data_model.events.data.events.asset.AssetDefinitionOwnerChanged")), ("Deleted", get_class("iroha_data_model.asset.DefinitionId")), ("MetadataInserted", get_class("iroha_data_model.events.data.events.MetadataChanged")), ("MetadataRemoved", get_class("iroha_data_model.events.data.events.MetadataChanged")), ("TotalQuantityChanged", get_class("iroha_data_model.events.data.events.asset.AssetDefinitionTotalQuantityChanged"))], typing.Union[get_class("iroha_data_model.asset.AssetDefinition"), get_class("iroha_data_model.asset.DefinitionId"), get_class("iroha_data_model.events.data.events.asset.AssetDefinitionOwnerChanged"), get_class("iroha_data_model.asset.DefinitionId"), get_class("iroha_data_model.events.data.events.MetadataChanged"), get_class("iroha_data_model.events.data.events.MetadataChanged"), get_class("iroha_data_model.events.data.events.asset.AssetDefinitionTotalQuantityChanged")])

AssetDefinitionEventFilter = make_enum("AssetDefinitionEventFilter", [("ByCreated", get_class(type(None))), ("ByMintabilityChanged", get_class(type(None))), ("ByOwnerChanged", get_class(type(None))), ("ByDeleted", get_class(type(None))), ("ByMetadataInserted", get_class(type(None))), ("ByMetadataRemoved", get_class(type(None))), ("ByTotalQuantityChanged", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None))])

AssetDefinitionFilter = make_struct("AssetDefinitionFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

AssetDefinitionOwnerChanged = make_struct("AssetDefinitionOwnerChanged", [("asset_definition_id", "iroha_data_model.asset.DefinitionId"), ("new_owner", "iroha_data_model.account.Id")])

AssetDefinitionTotalQuantityChanged = make_struct("AssetDefinitionTotalQuantityChanged", [("asset_definition_id", "iroha_data_model.asset.DefinitionId"), ("total_amount", "iroha_data_model.NumericValue")])

AssetEvent = make_enum("AssetEvent", [("Created", get_class("iroha_data_model.asset.Asset")), ("Deleted", get_class("iroha_data_model.asset.Id")), ("Added", get_class("iroha_data_model.events.data.events.asset.AssetChanged")), ("Removed", get_class("iroha_data_model.events.data.events.asset.AssetChanged")), ("MetadataInserted", get_class("iroha_data_model.events.data.events.MetadataChanged")), ("MetadataRemoved", get_class("iroha_data_model.events.data.events.MetadataChanged"))], typing.Union[get_class("iroha_data_model.asset.Asset"), get_class("iroha_data_model.asset.Id"), get_class("iroha_data_model.events.data.events.asset.AssetChanged"), get_class("iroha_data_model.events.data.events.asset.AssetChanged"), get_class("iroha_data_model.events.data.events.MetadataChanged"), get_class("iroha_data_model.events.data.events.MetadataChanged")])

AssetEventFilter = make_enum("AssetEventFilter", [("ByCreated", get_class(type(None))), ("ByDeleted", get_class(type(None))), ("ByAdded", get_class(type(None))), ("ByRemoved", get_class(type(None))), ("ByMetadataInserted", get_class(type(None))), ("ByMetadataRemoved", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None))])

AssetFilter = make_struct("AssetFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

SelfResolvingTypeVar.resolve_all()
