from ...rust import Enum, Struct, Tuple, Dict
Id = Struct[("name", "iroha_data_model.name.Name")]

NewRole = Struct[("inner", "iroha_data_model.role.Role")]

Role = Struct[("id", "iroha_data_model.role.Id"), ("permissions", list)]

