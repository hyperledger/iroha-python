from ......rust import Enum, Struct, Tuple, Dict
DomainEvent = Enum[("Account", "iroha_data_model.events.data.events.account.AccountEvent"), ("AssetDefinition", "iroha_data_model.events.data.events.asset.AssetDefinitionEvent"), ("Created", "iroha_data_model.domain.Id"), ("Deleted", "iroha_data_model.domain.Id"), ("MetadataInserted", "iroha_data_model.domain.Id"), ("MetadataRemoved", "iroha_data_model.domain.Id")] 
DomainEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None)), ("ByAccount", "iroha_data_model.events.data.filters.FilterOpt"), ("ByAssetDefinition", "iroha_data_model.events.data.filters.FilterOpt")] 
DomainFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

