from ....rust import Enum, Struct, Tuple, Dict
Predicate = Enum[("Contains", str), ("StartsWith", str), ("EndsWith", str), ("Is", str)] 
