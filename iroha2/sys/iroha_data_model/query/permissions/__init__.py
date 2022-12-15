
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
FindAllPermissionTokenDefinitions = make_tuple("FindAllPermissionTokenDefinitions")
FindPermissionTokensByAccountId = make_struct("FindPermissionTokensByAccountId", [("id", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
