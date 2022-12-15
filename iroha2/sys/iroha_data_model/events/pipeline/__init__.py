
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
EntityKind = make_enum("EntityKind", [("Block", get_class(type(None))), ("Transaction", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None))])

Event = make_struct("Event", [("entity_kind", "iroha_data_model.events.pipeline.EntityKind"), ("status", "iroha_data_model.events.pipeline.Status"), ("hash", "iroha_crypto.hash.Hash")])

EventFilter = make_struct("EventFilter", [("entity_kind", "iroha_data_model.events.pipeline.EntityKind"), ("status_kind", "iroha_data_model.events.pipeline.StatusKind"), ("hash", "iroha_crypto.hash.Hash")])

Status = make_enum("Status", [("Validating", get_class(type(None))), ("Rejected", get_class("iroha_data_model.transaction.RejectionReason")), ("Committed", get_class(type(None)))], typing.Union[get_class(type(None)), get_class("iroha_data_model.transaction.RejectionReason"), get_class(type(None))])

StatusKind = make_enum("StatusKind", [("Validating", get_class(type(None))), ("Rejected", get_class(type(None))), ("Committed", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None))])

SelfResolvingTypeVar.resolve_all()
