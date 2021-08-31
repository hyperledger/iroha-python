from ...rust import Enum, Struct, Tuple, Dict

Domain = Struct[("name", str), ("accounts", Dict), ("asset_definitions", Dict)]
