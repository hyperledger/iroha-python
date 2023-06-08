
from ..rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Duration = make_tuple("Duration", [int, int])
SelfResolvingTypeVar.resolve_all()
