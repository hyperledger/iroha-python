
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Pagination = make_struct("Pagination", [("start", int), ("limit", int)])

SelfResolvingTypeVar.resolve_all()
