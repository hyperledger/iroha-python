from ....rust import Enum, Struct, Tuple, Dict

FindAccountById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindAccountKeyValueByIdAndKey = Struct[(
    "id", "iroha_data_model.expression.EvaluatesTo"), (
        "key", "iroha_data_model.expression.EvaluatesTo")]

FindAccountsByDomainName = Struct[("domain_name",
                                   "iroha_data_model.expression.EvaluatesTo")]

FindAccountsByName = Struct[("name",
                             "iroha_data_model.expression.EvaluatesTo")]

FindAllAccounts = Struct[()]
