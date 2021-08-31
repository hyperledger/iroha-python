from ...rust import Enum, Struct, Tuple, Dict

PermissionToken = Struct[("name", str), ("params", Dict)]
