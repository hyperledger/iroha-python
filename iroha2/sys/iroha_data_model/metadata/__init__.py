
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Metadata = make_struct("Metadata", [("map", Dict)])

SelfResolvingTypeVar.resolve_all()
