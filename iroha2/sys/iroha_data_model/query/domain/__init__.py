from ....rust import Enum, make_struct, make_tuple, Dict
FindAllDomains = make_tuple("FindAllDomains")
FindDomainById = make_struct("FindDomainById", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindDomainKeyValueByIdAndKey = make_struct("FindDomainKeyValueByIdAndKey", [("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

