from ....rust import Enum, Struct, Tuple, Dict
Event = Struct[("trigger_id", "iroha_data_model.trigger.Id"), ("authority", "iroha_data_model.account.Id")]

EventFilter = Struct[("trigger_id", "iroha_data_model.trigger.Id"), ("authority", "iroha_data_model.account.Id")]

