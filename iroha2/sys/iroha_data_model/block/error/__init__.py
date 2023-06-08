
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
BlockRejectionReason = make_enum("BlockRejectionReason", [("ConsensusBlockRejection", get_class(type(None)))], typing.Union[get_class(type(None))])

SelfResolvingTypeVar.resolve_all()
