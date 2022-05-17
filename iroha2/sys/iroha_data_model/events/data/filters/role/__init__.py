from ......rust import Enum, Struct, Tuple, Dict
RoleEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None))] 
RoleFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

