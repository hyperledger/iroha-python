from ......rust import Enum, Struct, Tuple, Dict
DomainEventFilter = Enum[("ByAccount", "iroha_data_model.events.data.filters.FilterOpt"), ("ByAssetDefinition", "iroha_data_model.events.data.filters.FilterOpt"), ("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
DomainFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

