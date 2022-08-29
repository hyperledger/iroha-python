from ...rust import Enum, make_struct, make_tuple, Dict
Hash = make_tuple("Hash", [list])
HashOf = make_tuple("HashOf", ["iroha_crypto.hash.Hash"])
