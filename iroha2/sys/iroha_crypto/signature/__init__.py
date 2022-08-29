from ...rust import Enum, make_struct, make_tuple, Dict
Signature = make_struct("Signature", [("public_key", "iroha_crypto.PublicKey"), ("payload", list)])

SignatureOf = make_tuple("SignatureOf", ["iroha_crypto.signature.Signature"])
SignaturesOf = make_struct("SignaturesOf", [("signatures", Dict)])

