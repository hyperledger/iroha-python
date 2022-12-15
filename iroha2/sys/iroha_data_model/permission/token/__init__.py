
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Definition = make_struct("Definition", [("id", "iroha_data_model.permission.token.Id"), ("params", Dict)])

Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

Token = make_struct("Token", [("definition_id", "iroha_data_model.permission.token.Id"), ("params", Dict)])

SelfResolvingTypeVar.resolve_all()
