from ......rust import Enum, make_struct, make_tuple, Dict
RoleEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None))] 
RoleFilter = make_struct("RoleFilter", [("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

