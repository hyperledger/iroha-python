
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Predicate = make_enum("Predicate", [("Contains", get_class(str)), ("StartsWith", get_class(str)), ("EndsWith", get_class(str)), ("Is", get_class(str))], typing.Union[get_class(str), get_class(str), get_class(str), get_class(str)])

SelfResolvingTypeVar.resolve_all()
