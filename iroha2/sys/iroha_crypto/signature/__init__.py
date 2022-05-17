from ...rust import Enum, Struct, Tuple, Dict
Signature = Struct[("public_key", "iroha_crypto.PublicKey"), ("payload", list)]

SignatureOf = Tuple["iroha_crypto.signature.Signature"]
SignaturesOf = Struct[("signatures", Dict)]

