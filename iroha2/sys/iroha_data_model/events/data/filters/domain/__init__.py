from ......rust import Enum, make_struct, make_tuple, Dict
DomainEventFilter = Enum[("ByAccount", "iroha_data_model.events.data.filters.FilterOpt"), ("ByAssetDefinition", "iroha_data_model.events.data.filters.FilterOpt"), ("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
DomainFilter = make_struct("DomainFilter", [("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

