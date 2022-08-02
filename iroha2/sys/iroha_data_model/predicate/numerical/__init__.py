from ....rust import Enum, Struct, Tuple, Dict
Range = Enum[("U32", "iroha_data_model.predicate.numerical.SemiInterval"), ("U128", "iroha_data_model.predicate.numerical.SemiInterval"), ("Fixed", "iroha_data_model.predicate.numerical.SemiInterval")] 
SemiInterval = Struct[("start", "iroha_data_primitives.fixed.Fixed"), ("limit", "iroha_data_primitives.fixed.Fixed")]

