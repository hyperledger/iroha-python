from ..rust import Enum, Struct, Tuple, Dict

PublicKey = Struct[("digest_function", str), ("payload", list)]
