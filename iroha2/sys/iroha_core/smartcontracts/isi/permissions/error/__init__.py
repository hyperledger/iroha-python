from ......rust import Enum, make_struct, make_tuple, Dict
DenialReason = Enum[("ValidatorTypeMismatch", "iroha_core.smartcontracts.isi.error.Mismatch"), ("Custom", str), ("NoValidatorsProvided", type(None))] 
