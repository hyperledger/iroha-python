from ....rust import Enum, make_struct, make_tuple, Dict
FindAllRoleIds = make_tuple("FindAllRoleIds")
FindAllRoles = make_tuple("FindAllRoles")
FindRoleByRoleId = make_struct("FindRoleByRoleId", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindRolesByAccountId = make_struct("FindRolesByAccountId", [("id", "iroha_data_model.expression.EvaluatesTo")])

