from .....rust import Enum, Struct, Tuple, Dict
Error = Enum[("Decode", "iroha_version.error.Error"), ("Version", "iroha_core.smartcontracts.isi.query.UnsupportedVersionError"), ("Signature", str), ("Permission", str), ("Evaluate", str), ("Find", "iroha_core.smartcontracts.isi.error.FindError"), ("Conversion", str)] 
UnsupportedVersionError = Struct[("version", int)]

