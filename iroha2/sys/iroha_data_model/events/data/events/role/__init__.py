from ......rust import Enum, make_struct, make_tuple, Dict
RoleEvent = Enum[("Created", "iroha_data_model.role.Id"), ("Deleted", "iroha_data_model.role.Id")] 
RoleEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None))] 
RoleFilter = make_struct("RoleFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

