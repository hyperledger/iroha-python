
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Hash = make_tuple("Hash", [list])
HashOf = make_tuple("HashOf", ["iroha_crypto.hash.Hash"])
SelfResolvingTypeVar.resolve_all()
