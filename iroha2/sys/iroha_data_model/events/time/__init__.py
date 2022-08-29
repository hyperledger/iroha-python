from ....rust import Enum, make_struct, make_tuple, Dict
Event = make_struct("Event", [("prev_interval", "iroha_data_model.events.time.Interval"), ("interval", "iroha_data_model.events.time.Interval")])

EventFilter = make_tuple("EventFilter", ["iroha_data_model.events.time.ExecutionTime"])
ExecutionTime = Enum[("PreCommit", type(None)), ("Schedule", "iroha_data_model.events.time.Schedule")] 
Interval = make_struct("Interval", [("since", "Duration"), ("length", "Duration")])

Schedule = make_struct("Schedule", [("start", "Duration"), ("period", "Duration")])

