
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
AtIndex = make_struct("AtIndex", [("index", int), ("predicate", "iroha_data_model.predicate.value.Predicate")])

Container = make_enum("Container", [("Any", get_class("iroha_data_model.predicate.value.Predicate")), ("All", get_class("iroha_data_model.predicate.value.Predicate")), ("AtIndex", get_class("iroha_data_model.predicate.value.AtIndex")), ("ValueOfKey", get_class("iroha_data_model.predicate.value.ValueOfKey")), ("HasKey", get_class("iroha_data_model.name.Name"))], typing.Union[get_class("iroha_data_model.predicate.value.Predicate"), get_class("iroha_data_model.predicate.value.Predicate"), get_class("iroha_data_model.predicate.value.AtIndex"), get_class("iroha_data_model.predicate.value.ValueOfKey"), get_class("iroha_data_model.name.Name")])

Predicate = make_enum("Predicate", [("Identifiable", get_class("iroha_data_model.predicate.string.Predicate")), ("Container", get_class("iroha_data_model.predicate.value.Container")), ("Display", get_class("iroha_data_model.predicate.string.Predicate")), ("Numerical", get_class("iroha_data_model.predicate.numerical.SemiRange")), ("TimeStamp", get_class("iroha_data_model.predicate.numerical.SemiInterval")), ("Ipv4Addr", get_class("iroha_data_model.predicate.ip_addr.Ipv4Predicate")), ("Ipv6Addr", get_class("iroha_data_model.predicate.ip_addr.Ipv6Predicate")), ("Pass", get_class(type(None)))], typing.Union[get_class("iroha_data_model.predicate.string.Predicate"), get_class("iroha_data_model.predicate.value.Container"), get_class("iroha_data_model.predicate.string.Predicate"), get_class("iroha_data_model.predicate.numerical.SemiRange"), get_class("iroha_data_model.predicate.numerical.SemiInterval"), get_class("iroha_data_model.predicate.ip_addr.Ipv4Predicate"), get_class("iroha_data_model.predicate.ip_addr.Ipv6Predicate"), get_class(type(None))])

ValueOfKey = make_struct("ValueOfKey", [("key", "iroha_data_model.name.Name"), ("predicate", "iroha_data_model.predicate.value.Predicate")])

SelfResolvingTypeVar.resolve_all()
