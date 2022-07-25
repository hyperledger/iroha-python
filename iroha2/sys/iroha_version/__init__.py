from ..rust import Enum, make_struct, make_tuple, Dict
RawVersioned = Enum[("Json", str), ("ScaleBytes", list)] 
UnsupportedVersion = make_struct("UnsupportedVersion", [("version", int), ("raw", "iroha_version.RawVersioned")])

