
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Topology = make_struct("Topology", [("sorted_peers", list), ("at_block", "iroha_crypto.hash.HashOf")])

SelfResolvingTypeVar.resolve_all()
