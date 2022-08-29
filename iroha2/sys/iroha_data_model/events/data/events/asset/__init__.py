from ......rust import Enum, make_struct, make_tuple, Dict
AssetDefinitionEvent = Enum[("Created", "iroha_data_model.asset.DefinitionId"), ("MintabilityChanged", "iroha_data_model.asset.DefinitionId"), ("Deleted", "iroha_data_model.asset.DefinitionId"), ("MetadataInserted", "iroha_data_model.asset.DefinitionId"), ("MetadataRemoved", "iroha_data_model.asset.DefinitionId")] 
AssetDefinitionEventFilter = Enum[("ByCreated", type(None)), ("ByMintabilityChanged", type(None)), ("ByDeleted", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AssetDefinitionFilter = make_struct("AssetDefinitionFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

AssetEvent = Enum[("Created", "iroha_data_model.asset.Id"), ("Deleted", "iroha_data_model.asset.Id"), ("Added", "iroha_data_model.asset.Id"), ("Removed", "iroha_data_model.asset.Id"), ("MetadataInserted", "iroha_data_model.asset.Id"), ("MetadataRemoved", "iroha_data_model.asset.Id")] 
AssetEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByAdded", type(None)), ("ByRemoved", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AssetFilter = make_struct("AssetFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

