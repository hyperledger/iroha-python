from ......rust import Enum, make_struct, make_tuple, Dict
TriggerEvent = Enum[("Created", "iroha_data_model.trigger.Id"), ("Deleted", "iroha_data_model.trigger.Id"), ("Extended", "iroha_data_model.trigger.Id"), ("Shortened", "iroha_data_model.trigger.Id")] 
TriggerEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByExtended", type(None)), ("ByShortened", type(None))] 
TriggerFilter = make_struct("TriggerFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

