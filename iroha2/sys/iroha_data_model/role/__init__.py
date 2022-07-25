from ...rust import Enum, make_struct, make_tuple, Dict
Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

NewRole = make_struct("NewRole", [("inner", "iroha_data_model.role.Role")])

Role = make_struct("Role", [("id", "iroha_data_model.role.Id"), ("permissions", list)])

