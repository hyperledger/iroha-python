
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Interval = make_struct("Interval", [("start", int), ("limit", int)])

SemiInterval = make_struct("SemiInterval", [("start", "iroha_primitives.fixed.Fixed"), ("limit", "iroha_primitives.fixed.Fixed")])

SemiRange = make_enum("SemiRange", [("U32", get_class("iroha_data_model.predicate.numerical.SemiInterval")), ("U128", get_class("iroha_data_model.predicate.numerical.SemiInterval")), ("Fixed", get_class("iroha_data_model.predicate.numerical.SemiInterval"))], typing.Union[get_class("iroha_data_model.predicate.numerical.SemiInterval"), get_class("iroha_data_model.predicate.numerical.SemiInterval"), get_class("iroha_data_model.predicate.numerical.SemiInterval")])

SelfResolvingTypeVar.resolve_all()
