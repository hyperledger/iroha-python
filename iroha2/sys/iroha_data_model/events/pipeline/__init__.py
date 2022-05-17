from ....rust import Enum, Struct, Tuple, Dict
EntityKind = Enum[("Block", type(None)), ("Transaction", type(None))] 
Event = Struct[("entity_kind", "iroha_data_model.events.pipeline.EntityKind"), ("status", "iroha_data_model.events.pipeline.Status"), ("hash", "iroha_crypto.hash.Hash")]

EventFilter = Struct[("entity_kind", "iroha_data_model.events.pipeline.EntityKind"), ("status_kind", "iroha_data_model.events.pipeline.StatusKind"), ("hash", "iroha_crypto.hash.Hash")]

Status = Enum[("Validating", type(None)), ("Rejected", "iroha_data_model.transaction.RejectionReason"), ("Committed", type(None))] 
StatusKind = Enum[("Validating", type(None)), ("Rejected", type(None)), ("Committed", type(None))] 
