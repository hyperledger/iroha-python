
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
FindAllRoleIds = make_tuple("FindAllRoleIds")
FindAllRoles = make_tuple("FindAllRoles")
FindRoleByRoleId = make_struct("FindRoleByRoleId", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindRolesByAccountId = make_struct("FindRolesByAccountId", [("id", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
