from ....rust import Enum, Struct, Tuple, Dict
FindAllDomains = Tuple[()]
FindDomainById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindDomainKeyValueByIdAndKey = Struct[("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")]

