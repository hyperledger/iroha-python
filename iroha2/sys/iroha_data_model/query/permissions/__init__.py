
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
DoesAccountHavePermissionToken = make_struct("DoesAccountHavePermissionToken", [("account_id", "iroha_data_model.expression.EvaluatesTo"), ("permission_token", "iroha_data_model.permission.token.Token")])

FindAllPermissionTokenDefinitions = make_tuple("FindAllPermissionTokenDefinitions")
FindPermissionTokensByAccountId = make_struct("FindPermissionTokensByAccountId", [("id", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
