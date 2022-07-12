from ...rust import Enum, Struct, Tuple, Dict
PredicateBox = Enum[("And", list), ("Or", list), ("Not", "iroha_data_model.predicate.PredicateBox"), ("Raw", "iroha_data_model.predicate.value.Predicate")] 
