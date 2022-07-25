from ...rust import Enum, make_struct, make_tuple, Dict
PredicateBox = Enum[("And", list), ("Or", list), ("Not", "iroha_data_model.predicate.PredicateBox"), ("Raw", "iroha_data_model.predicate.value.Predicate")] 
