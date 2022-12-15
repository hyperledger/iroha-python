
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Id = make_struct("Id", [("address", str), ("public_key", "iroha_crypto.PublicKey")])

Peer = make_struct("Peer", [("id", "iroha_data_model.peer.Id")])

SelfResolvingTypeVar.resolve_all()
