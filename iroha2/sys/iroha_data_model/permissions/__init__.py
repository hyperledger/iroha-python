from ...rust import Enum, make_struct, make_tuple, Dict
Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

PermissionToken = make_struct("PermissionToken", [("definition_id", "iroha_data_model.permissions.Id"), ("params", Dict)])

PermissionTokenDefinition = make_struct("PermissionTokenDefinition", [("id", "iroha_data_model.permissions.Id")])

