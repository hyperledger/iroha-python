from ......rust import Enum, make_struct, make_tuple, Dict
TriggerEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByExtended", type(None)), ("ByShortened", type(None))] 
TriggerFilter = make_struct("TriggerFilter", [("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

