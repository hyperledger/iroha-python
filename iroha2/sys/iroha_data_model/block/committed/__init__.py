
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
CommittedBlock = make_struct("CommittedBlock", [("header", "iroha_data_model.block.header.BlockHeader"), ("rejected_transactions", list), ("transactions", list), ("event_recommendations", list), ("signatures", "iroha_crypto.signature.SignaturesOf")])

VersionedCommittedBlock = make_enum("VersionedCommittedBlock", [("V1", get_class("iroha_data_model.block.committed.CommittedBlock"))], typing.Union[get_class("iroha_data_model.block.committed.CommittedBlock")])

SelfResolvingTypeVar.resolve_all()
