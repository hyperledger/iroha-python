
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Event = make_struct("Event", [("trigger_id", "iroha_data_model.trigger.Id"), ("authority", "iroha_data_model.account.Id")])

EventFilter = make_struct("EventFilter", [("trigger_id", "iroha_data_model.trigger.Id"), ("authority", "iroha_data_model.account.Id")])

SelfResolvingTypeVar.resolve_all()
