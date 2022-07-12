from ......rust import Enum, Struct, Tuple, Dict
AccountEventFilter = Enum[("ByAsset", "iroha_data_model.events.data.filters.FilterOpt"), ("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByAuthenticationAdded", type(None)), ("ByAuthenticationRemoved", type(None)), ("ByPermissionAdded", type(None)), ("ByPermissionRemoved", type(None)), ("ByRoleRevoked", type(None)), ("ByRoleGranted", type(None)), ("ByMetadataInserted", type(None)), ("ByMetadataRemoved", type(None))] 
AccountFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

