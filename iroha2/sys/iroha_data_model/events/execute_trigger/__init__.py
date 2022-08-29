from ....rust import Enum, make_struct, make_tuple, Dict
Event = make_struct("Event", [("trigger_id", "iroha_data_model.trigger.Id"), ("authority", "iroha_data_model.account.Id")])

EventFilter = make_struct("EventFilter", [("trigger_id", "iroha_data_model.trigger.Id"), ("authority", "iroha_data_model.account.Id")])

