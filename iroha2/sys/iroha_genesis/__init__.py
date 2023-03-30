
from ..rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
GenesisTransaction = make_struct("GenesisTransaction", [("isi", list)])

RawGenesisBlock = make_struct("RawGenesisBlock", [("transactions", list)])

SelfResolvingTypeVar.resolve_all()
