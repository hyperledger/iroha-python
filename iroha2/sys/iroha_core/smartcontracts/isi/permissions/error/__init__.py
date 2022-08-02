from ......rust import Enum, Struct, Tuple, Dict
DenialReason = Enum[("ValidatorTypeMismatch", "iroha_core.smartcontracts.isi.error.Mismatch"), ("Custom", str), ("NoValidatorsProvided", type(None))] 
