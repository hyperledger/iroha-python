
from ..rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
RawVersioned = make_enum("RawVersioned", [("Json", get_class(str)), ("ScaleBytes", get_class(list))], typing.Union[get_class(str), get_class(list)])

UnsupportedVersion = make_struct("UnsupportedVersion", [("version", int), ("raw", "iroha_version.RawVersioned")])

SelfResolvingTypeVar.resolve_all()
