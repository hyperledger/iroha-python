from ...rust import Enum, Struct, Tuple, Dict

Id = Struct[("address", str), ("public_key", "iroha_crypto.PublicKey")]

Peer = Struct[("id", "iroha_data_model.peer.Id")]
