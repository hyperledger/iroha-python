
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Event = make_enum("Event", [("Pipeline", get_class("iroha_data_model.events.pipeline.Event")), ("Data", get_class("iroha_data_model.events.data.events.Event")), ("Time", get_class("iroha_data_model.events.time.Event")), ("ExecuteTrigger", get_class("iroha_data_model.events.execute_trigger.Event"))], typing.Union[get_class("iroha_data_model.events.pipeline.Event"), get_class("iroha_data_model.events.data.events.Event"), get_class("iroha_data_model.events.time.Event"), get_class("iroha_data_model.events.execute_trigger.Event")])

FilterBox = make_enum("FilterBox", [("Pipeline", get_class("iroha_data_model.events.pipeline.EventFilter")), ("Data", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("Time", get_class("iroha_data_model.events.time.EventFilter")), ("ExecuteTrigger", get_class("iroha_data_model.events.execute_trigger.EventFilter"))], typing.Union[get_class("iroha_data_model.events.pipeline.EventFilter"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.time.EventFilter"), get_class("iroha_data_model.events.execute_trigger.EventFilter")])

SelfResolvingTypeVar.resolve_all()
