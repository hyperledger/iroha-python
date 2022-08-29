from ...rust import Enum, make_struct, make_tuple, Dict
Error = Enum[("NotVersioned", type(None)), ("UnsupportedJsonEncode", type(None)), ("ExpectedJson", type(None)), ("UnsupportedScaleEncode", type(None)), ("Serde", type(None)), ("ParityScale", type(None)), ("ParseInt", type(None)), ("UnsupportedVersion", "iroha_version.UnsupportedVersion"), ("ExtraBytesLeft", int)] 
