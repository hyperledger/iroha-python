
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
NonTrivial = make_tuple("NonTrivial", [list])
SelfResolvingTypeVar.resolve_all()
