from .....rust import Enum, make_struct, make_tuple, Dict
Error = Enum[("Decode", "iroha_version.error.Error"), ("Signature", str), ("Permission", str), ("Evaluate", str), ("Find", "iroha_core.smartcontracts.isi.error.FindError"), ("Conversion", str), ("Unauthorized", type(None))] 
