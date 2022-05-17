from ....rust import Enum, Struct, Tuple, Dict
FindAllRoleIds = Tuple[()]
FindAllRoles = Tuple[()]
FindRoleByRoleId = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindRolesByAccountId = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

