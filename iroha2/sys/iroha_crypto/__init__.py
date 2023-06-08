
from ..rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
PublicKey = make_struct("PublicKey", [("digest_function", str), ("payload", list)])

SelfResolvingTypeVar.resolve_all()
