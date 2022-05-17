from ....rust import Enum, Struct, Tuple, Dict
FindAccountById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindAccountKeyValueByIdAndKey = Struct[("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")]

FindAccountsByDomainId = Struct[("domain_id", "iroha_data_model.expression.EvaluatesTo")]

FindAccountsByName = Struct[("name", "iroha_data_model.expression.EvaluatesTo")]

FindAccountsWithAsset = Struct[("asset_definition_id", "iroha_data_model.expression.EvaluatesTo")]

FindAllAccounts = Tuple[()]
