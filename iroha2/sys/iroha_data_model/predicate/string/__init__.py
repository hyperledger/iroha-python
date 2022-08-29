from ....rust import Enum, make_struct, make_tuple, Dict
Predicate = Enum[("Contains", str), ("StartsWith", str), ("EndsWith", str), ("Is", str)] 
