
from .....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Error = make_enum("Error", [("Decode", get_class("iroha_version.error.Error")), ("Signature", get_class(str)), ("Permission", get_class(str)), ("Evaluate", get_class(str)), ("Find", get_class("iroha_core.smartcontracts.isi.error.FindError")), ("Conversion", get_class(str)), ("Unauthorized", get_class(type(None)))], typing.Union[get_class("iroha_version.error.Error"), get_class(str), get_class(str), get_class(str), get_class("iroha_core.smartcontracts.isi.error.FindError"), get_class(str), get_class(type(None))])

SelfResolvingTypeVar.resolve_all()
