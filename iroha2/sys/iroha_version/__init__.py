from ..rust import Enum, Struct, Tuple, Dict
RawVersioned = Enum[("Json", str), ("ScaleBytes", list)] 
UnsupportedVersion = Struct[("version", int), ("raw", "iroha_version.RawVersioned")]

