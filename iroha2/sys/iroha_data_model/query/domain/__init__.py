from ....rust import Enum, Struct, Tuple, Dict

FindAllDomains = Struct[()]

FindDomainByName = Struct[("name", "iroha_data_model.expression.EvaluatesTo")]

FindDomainKeyValueByIdAndKey = Struct[(
    "name", "iroha_data_model.expression.EvaluatesTo"), (
        "key", "iroha_data_model.expression.EvaluatesTo")]
