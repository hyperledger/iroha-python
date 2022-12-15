
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Action = make_struct("Action", [("executable", "iroha_data_model.transaction.Executable"), ("repeats", "iroha_data_model.trigger.action.Repeats"), ("technical_account", "iroha_data_model.account.Id"), ("filter", "iroha_data_model.events.FilterBox"), ("metadata", "iroha_data_model.metadata.Metadata")])

Repeats = make_enum("Repeats", [("Indefinitely", get_class(type(None))), ("Exactly", get_class("AtomicU32Wrapper"))], typing.Union[get_class(type(None)), get_class("AtomicU32Wrapper")])

SelfResolvingTypeVar.resolve_all()
