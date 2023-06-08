
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Signature = make_struct("Signature", [("public_key", "iroha_crypto.PublicKey"), ("payload", list)])

SignatureOf = make_tuple("SignatureOf", ["iroha_crypto.signature.Signature"])
SignaturesOf = make_struct("SignaturesOf", [("signatures", list)])

SelfResolvingTypeVar.resolve_all()
