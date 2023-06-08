
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Event = make_enum("Event", [("Pipeline", get_class("iroha_data_model.events.pipeline.Event")), ("Data", get_class("iroha_data_model.events.data.events.Event")), ("Time", get_class("iroha_data_model.events.time.Event")), ("ExecuteTrigger", get_class("iroha_data_model.events.execute_trigger.Event"))], typing.Union[get_class("iroha_data_model.events.pipeline.Event"), get_class("iroha_data_model.events.data.events.Event"), get_class("iroha_data_model.events.time.Event"), get_class("iroha_data_model.events.execute_trigger.Event")])

EventMessage = make_tuple("EventMessage", ["iroha_data_model.events.Event"])
EventSubscriptionRequest = make_tuple("EventSubscriptionRequest", ["iroha_data_model.events.FilterBox"])
FilterBox = make_enum("FilterBox", [("Pipeline", get_class("iroha_data_model.events.pipeline.EventFilter")), ("Data", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("Time", get_class("iroha_data_model.events.time.EventFilter")), ("ExecuteTrigger", get_class("iroha_data_model.events.execute_trigger.EventFilter"))], typing.Union[get_class("iroha_data_model.events.pipeline.EventFilter"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.time.EventFilter"), get_class("iroha_data_model.events.execute_trigger.EventFilter")])

VersionedEventMessage = make_enum("VersionedEventMessage", [("V1", get_class("iroha_data_model.events.EventMessage"))], typing.Union[get_class("iroha_data_model.events.EventMessage")])

VersionedEventSubscriptionRequest = make_enum("VersionedEventSubscriptionRequest", [("V1", get_class("iroha_data_model.events.EventSubscriptionRequest"))], typing.Union[get_class("iroha_data_model.events.EventSubscriptionRequest")])

SelfResolvingTypeVar.resolve_all()
