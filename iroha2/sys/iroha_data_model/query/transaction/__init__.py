from ....rust import Enum, Struct, Tuple, Dict
FindAllTransactions = Tuple[()]
FindTransactionByHash = Struct[("hash", "iroha_data_model.expression.EvaluatesTo")]

FindTransactionsByAccountId = Struct[("account_id", "iroha_data_model.expression.EvaluatesTo")]

