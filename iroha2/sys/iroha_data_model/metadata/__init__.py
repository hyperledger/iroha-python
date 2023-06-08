
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Limits = make_struct("Limits", [("max_len", int), ("max_entry_byte_size", int)])

Metadata = make_struct("Metadata", [("map", Dict)])

SelfResolvingTypeVar.resolve_all()
