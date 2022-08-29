from ......rust import Enum, make_struct, make_tuple, Dict
PeerEvent = Enum[("Added", "iroha_data_model.peer.Id"), ("Removed", "iroha_data_model.peer.Id")] 
PeerEventFilter = Enum[("ByAdded", type(None)), ("ByRemoved", type(None))] 
PeerFilter = make_struct("PeerFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

