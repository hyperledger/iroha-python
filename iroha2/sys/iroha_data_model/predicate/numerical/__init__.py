from ....rust import Enum, make_struct, make_tuple, Dict
Interval = make_struct("Interval", [("start", int), ("limit", int)])

SemiInterval = make_struct("SemiInterval", [("start", "iroha_primitives.fixed.Fixed"), ("limit", "iroha_primitives.fixed.Fixed")])

SemiRange = Enum[("U32", "iroha_data_model.predicate.numerical.SemiInterval"), ("U128", "iroha_data_model.predicate.numerical.SemiInterval"), ("Fixed", "iroha_data_model.predicate.numerical.SemiInterval")] 
