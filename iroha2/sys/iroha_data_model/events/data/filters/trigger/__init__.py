from ......rust import Enum, Struct, Tuple, Dict
TriggerEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByExtended", type(None)), ("ByShortened", type(None))] 
TriggerFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

