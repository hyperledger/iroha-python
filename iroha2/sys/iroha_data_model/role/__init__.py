from ...rust import Enum, Struct, Tuple, Dict
Id = Struct[("name", "iroha_data_model.Name")]

Role = Struct[("id", "iroha_data_model.role.Id"), ("permissions", list)]

