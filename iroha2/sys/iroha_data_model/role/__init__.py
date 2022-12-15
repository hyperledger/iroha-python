
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

NewRole = make_struct("NewRole", [("inner", "iroha_data_model.role.Role")])

Role = make_struct("Role", [("id", "iroha_data_model.role.Id"), ("permissions", list)])

SelfResolvingTypeVar.resolve_all()
