from ....rust import Enum, Struct, Tuple, Dict

FindTransactionsByAccountId = Struct[(
    "account_id", "iroha_data_model.expression.EvaluatesTo")]
