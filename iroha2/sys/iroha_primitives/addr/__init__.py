
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Ipv4Addr = make_tuple("Ipv4Addr", [list])
Ipv6Addr = make_tuple("Ipv6Addr", [list])
SelfResolvingTypeVar.resolve_all()
