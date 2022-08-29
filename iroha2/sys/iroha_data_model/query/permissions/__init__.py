from ....rust import Enum, make_struct, make_tuple, Dict
FindAllPermissionTokenDefinitions = make_tuple("FindAllPermissionTokenDefinitions")
FindPermissionTokensByAccountId = make_struct("FindPermissionTokensByAccountId", [("id", "iroha_data_model.expression.EvaluatesTo")])

