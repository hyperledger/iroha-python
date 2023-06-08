
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Error = make_enum("Error", [("NotVersioned", get_class(type(None))), ("UnsupportedJsonEncode", get_class(type(None))), ("ExpectedJson", get_class(type(None))), ("UnsupportedScaleEncode", get_class(type(None))), ("Serde", get_class(type(None))), ("ParityScale", get_class(type(None))), ("ParseInt", get_class(type(None))), ("UnsupportedVersion", get_class("iroha_version.UnsupportedVersion")), ("ExtraBytesLeft", get_class(int))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class("iroha_version.UnsupportedVersion"), get_class(int)])

SelfResolvingTypeVar.resolve_all()
