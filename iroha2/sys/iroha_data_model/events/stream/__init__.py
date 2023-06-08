
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
EventMessage = make_tuple("EventMessage", ["iroha_data_model.events.Event"])
EventSubscriptionRequest = make_tuple("EventSubscriptionRequest", ["iroha_data_model.events.FilterBox"])
VersionedEventMessage = make_enum("VersionedEventMessage", [("V1", get_class("iroha_data_model.events.stream.EventMessage"))], typing.Union[get_class("iroha_data_model.events.stream.EventMessage")])

VersionedEventSubscriptionRequest = make_enum("VersionedEventSubscriptionRequest", [("V1", get_class("iroha_data_model.events.stream.EventSubscriptionRequest"))], typing.Union[get_class("iroha_data_model.events.stream.EventSubscriptionRequest")])

SelfResolvingTypeVar.resolve_all()
