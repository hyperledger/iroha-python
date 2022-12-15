
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
FindAllTransactions = make_tuple("FindAllTransactions")
FindTransactionByHash = make_struct("FindTransactionByHash", [("hash", "iroha_data_model.expression.EvaluatesTo")])

FindTransactionsByAccountId = make_struct("FindTransactionsByAccountId", [("account_id", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
