from .....rust import Enum, Struct, Tuple, Dict
Error = Enum[("Decode", "iroha_version.error.Error"), ("Signature", str), ("Permission", "iroha_core.smartcontracts.isi.permissions.error.DenialReason"), ("Evaluate", str), ("Find", "iroha_core.smartcontracts.isi.error.FindError"), ("Conversion", str), ("Unauthorized", type(None))] 
