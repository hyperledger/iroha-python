from ....rust import Enum, make_struct, make_tuple, Dict
FindAllBlockHeaders = make_tuple("FindAllBlockHeaders")
FindAllBlocks = make_tuple("FindAllBlocks")
FindBlockHeaderByHash = make_struct("FindBlockHeaderByHash", [("hash", "iroha_data_model.expression.EvaluatesTo")])

