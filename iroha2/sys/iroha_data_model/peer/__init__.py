from ...rust import Enum, make_struct, make_tuple, Dict
Id = make_struct("Id", [("address", str), ("public_key", "iroha_crypto.PublicKey")])

Peer = make_struct("Peer", [("id", "iroha_data_model.peer.Id")])

