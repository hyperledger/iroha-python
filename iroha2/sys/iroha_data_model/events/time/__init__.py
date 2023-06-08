
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Event = make_struct("Event", [("prev_interval", "iroha_data_model.events.time.Interval"), ("interval", "iroha_data_model.events.time.Interval")])

EventFilter = make_tuple("EventFilter", ["iroha_data_model.events.time.ExecutionTime"])
ExecutionTime = make_enum("ExecutionTime", [("PreCommit", get_class(type(None))), ("Schedule", get_class("iroha_data_model.events.time.Schedule"))], typing.Union[get_class(type(None)), get_class("iroha_data_model.events.time.Schedule")])

Interval = make_struct("Interval", [("since", "Duration"), ("length", "Duration")])

Schedule = make_struct("Schedule", [("start", "Duration"), ("period", "Duration")])

SelfResolvingTypeVar.resolve_all()
