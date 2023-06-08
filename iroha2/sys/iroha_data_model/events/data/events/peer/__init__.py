
from ......rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
PeerEvent = make_enum("PeerEvent", [("Added", get_class("iroha_data_model.peer.Id")), ("Removed", get_class("iroha_data_model.peer.Id"))], typing.Union[get_class("iroha_data_model.peer.Id"), get_class("iroha_data_model.peer.Id")])

PeerEventFilter = make_enum("PeerEventFilter", [("ByAdded", get_class(type(None))), ("ByRemoved", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None))])

PeerFilter = make_struct("PeerFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

SelfResolvingTypeVar.resolve_all()
