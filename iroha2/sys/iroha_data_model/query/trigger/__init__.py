from ....rust import Enum, Struct, Tuple, Dict
FindAllActiveTriggerIds = Tuple[()]
FindTriggerById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindTriggerKeyValueByIdAndKey = Struct[("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")]

FindTriggersByDomainId = Struct[("domain_id", "iroha_data_model.expression.EvaluatesTo")]

