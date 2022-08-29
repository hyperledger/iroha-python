from ......rust import Enum, make_struct, make_tuple, Dict
PeerEventFilter = Enum[("ByAdded", type(None)), ("ByRemoved", type(None))] 
PeerFilter = make_struct("PeerFilter", [("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

