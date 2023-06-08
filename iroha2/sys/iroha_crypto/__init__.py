
from ..rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Algorithm = make_enum("Algorithm", [("Ed25519", get_class(type(None))), ("Secp256k1", get_class(type(None))), ("BlsNormal", get_class(type(None))), ("BlsSmall", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None))])

PublicKey = make_struct("PublicKey", [("digest_function", "iroha_crypto.Algorithm"), ("payload", list)])

SelfResolvingTypeVar.resolve_all()
