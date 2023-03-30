
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

Parameter = make_struct("Parameter", [("id", "iroha_data_model.parameter.Id"), ("val", "iroha_data_model.Value")])

SelfResolvingTypeVar.resolve_all()
