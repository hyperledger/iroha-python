from ....rust import Enum, make_struct, make_tuple, Dict
FindAllTransactions = make_tuple("FindAllTransactions")
FindTransactionByHash = make_struct("FindTransactionByHash", [("hash", "iroha_data_model.expression.EvaluatesTo")])

FindTransactionsByAccountId = make_struct("FindTransactionsByAccountId", [("account_id", "iroha_data_model.expression.EvaluatesTo")])

