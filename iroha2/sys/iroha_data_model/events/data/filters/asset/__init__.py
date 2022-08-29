from ......rust import Enum, make_struct, make_tuple, Dict
AssetDefinitionEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByMintabilityChanged", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AssetDefinitionFilter = make_struct("AssetDefinitionFilter", [("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

AssetEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByAdded", type(None)), ("ByRemoved", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AssetFilter = make_struct("AssetFilter", [("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

