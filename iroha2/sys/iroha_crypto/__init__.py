from ..rust import Enum, make_struct, make_tuple, Dict
PublicKey = make_struct("PublicKey", [("digest_function", str), ("payload", list)])

