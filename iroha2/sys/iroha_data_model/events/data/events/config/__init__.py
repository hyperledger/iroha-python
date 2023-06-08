
from ......rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
ConfigurationEvent = make_enum("ConfigurationEvent", [("Changed", get_class("iroha_data_model.parameter.Id")), ("Created", get_class("iroha_data_model.parameter.Id")), ("Deleted", get_class("iroha_data_model.parameter.Id"))], typing.Union[get_class("iroha_data_model.parameter.Id"), get_class("iroha_data_model.parameter.Id"), get_class("iroha_data_model.parameter.Id")])

SelfResolvingTypeVar.resolve_all()
