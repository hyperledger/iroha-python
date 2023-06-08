
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
GenericPredicateBox = make_enum("GenericPredicateBox", [("And", get_class("iroha_data_model.predicate.nontrivial.NonTrivial")), ("Or", get_class("iroha_data_model.predicate.nontrivial.NonTrivial")), ("Not", get_class("iroha_data_model.predicate.GenericPredicateBox")), ("Raw", get_class("iroha_data_model.predicate.value.Predicate"))], typing.Union[get_class("iroha_data_model.predicate.nontrivial.NonTrivial"), get_class("iroha_data_model.predicate.nontrivial.NonTrivial"), get_class("iroha_data_model.predicate.GenericPredicateBox"), get_class("iroha_data_model.predicate.value.Predicate")])

SelfResolvingTypeVar.resolve_all()
