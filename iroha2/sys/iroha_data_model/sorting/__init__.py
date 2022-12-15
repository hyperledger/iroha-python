
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Sorting = make_struct("Sorting", [("sort_by_metadata_key", "iroha_data_model.name.Name")])

SelfResolvingTypeVar.resolve_all()
