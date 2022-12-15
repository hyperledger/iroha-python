
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
FindAllBlockHeaders = make_tuple("FindAllBlockHeaders")
FindAllBlocks = make_tuple("FindAllBlocks")
FindBlockHeaderByHash = make_struct("FindBlockHeaderByHash", [("hash", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
