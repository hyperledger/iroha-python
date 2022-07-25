from ...rust import Enum, make_struct, make_tuple, Dict
PermissionToken = make_struct("PermissionToken", [("name", "iroha_data_model.name.Name"), ("params", Dict)])

