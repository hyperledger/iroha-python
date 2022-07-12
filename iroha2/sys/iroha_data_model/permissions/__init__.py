from ...rust import Enum, Struct, Tuple, Dict
PermissionToken = Struct[("name", "iroha_data_model.name.Name"), ("params", Dict)]

