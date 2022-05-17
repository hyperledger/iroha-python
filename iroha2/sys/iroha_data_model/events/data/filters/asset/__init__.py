from ......rust import Enum, Struct, Tuple, Dict
AssetDefinitionEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByMintabilityChanged", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AssetDefinitionFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

AssetEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByAdded", type(None)), ("ByRemoved", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AssetFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

