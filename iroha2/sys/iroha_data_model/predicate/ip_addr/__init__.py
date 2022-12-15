
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Ipv4Predicate = make_tuple("Ipv4Predicate", [list])
Ipv6Predicate = make_tuple("Ipv6Predicate", [list])
SelfResolvingTypeVar.resolve_all()
