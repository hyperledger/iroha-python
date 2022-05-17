from ....rust import Enum, Struct, Tuple, Dict
Event = Struct[("prev_interval", "iroha_data_model.events.time.Interval"), ("interval", "iroha_data_model.events.time.Interval")]

EventFilter = Tuple["iroha_data_model.events.time.ExecutionTime"]
ExecutionTime = Enum[("PreCommit", type(None)), ("Schedule", "iroha_data_model.events.time.Schedule")] 
Interval = Struct[("since", "Duration"), ("length", "Duration")]

Schedule = Struct[("start", "Duration"), ("period", "Duration")]

