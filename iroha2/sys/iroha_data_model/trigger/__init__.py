from ...rust import Enum, Struct, Tuple, Dict
Id = Struct[("name", "iroha_data_model.Name")]

Trigger = Struct[("id", "iroha_data_model.trigger.Id"), ("action", "iroha_data_model.trigger.action.Action")]

