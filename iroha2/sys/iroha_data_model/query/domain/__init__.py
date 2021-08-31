from ....rust import Enum, Struct, Tuple, Dict

FindAllDomains = Struct[()]

FindDomainByName = Struct[("name", "iroha_data_model.expression.EvaluatesTo")]
