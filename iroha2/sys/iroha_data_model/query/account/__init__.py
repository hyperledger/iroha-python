from ....rust import Enum, make_struct, make_tuple, Dict
FindAccountById = make_struct("FindAccountById", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindAccountKeyValueByIdAndKey = make_struct("FindAccountKeyValueByIdAndKey", [("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

FindAccountsByDomainId = make_struct("FindAccountsByDomainId", [("domain_id", "iroha_data_model.expression.EvaluatesTo")])

FindAccountsByName = make_struct("FindAccountsByName", [("name", "iroha_data_model.expression.EvaluatesTo")])

FindAccountsWithAsset = make_struct("FindAccountsWithAsset", [("asset_definition_id", "iroha_data_model.expression.EvaluatesTo")])

FindAllAccounts = make_tuple("FindAllAccounts")
