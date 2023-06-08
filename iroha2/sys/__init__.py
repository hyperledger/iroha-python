from ..iroha2 import *

from .rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
SelfResolvingTypeVar.resolve_all()
