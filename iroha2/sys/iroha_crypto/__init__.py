from ..rust import Enum, Struct, Tuple, Dict

Hash = Tuple[list]
PublicKey = Struct[("digest_function", str), ("payload", list)]

Signature = Struct[("public_key", "iroha_crypto.PublicKey"),
                   ("signature", list)]
