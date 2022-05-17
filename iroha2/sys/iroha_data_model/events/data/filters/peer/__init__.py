from ......rust import Enum, Struct, Tuple, Dict
PeerEventFilter = Enum[("ByAdded", type(None)), ("ByRemoved", type(None))] 
PeerFilter = Struct[("id_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")]

