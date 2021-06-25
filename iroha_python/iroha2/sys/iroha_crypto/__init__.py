from ..rust import Enum, Struct, Tuple, Dict
PublicKey = Struct[("digest_function", str), ("payload", list)]

Signature = Struct[("public_key", "iroha_crypto.PublicKey"), ("signature", list)]

