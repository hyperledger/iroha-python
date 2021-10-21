from ...rust import Enum, Struct, Tuple, Dict

Signature = Struct[("public_key", "iroha_crypto.PublicKey"),
                   ("signature", list)]

SignatureVerificationFail = Struct[("signature",
                                    "iroha_crypto.signature.Signature"),
                                   ("reason", str)]

SignaturesOf = Struct[("signatures", Dict)]
