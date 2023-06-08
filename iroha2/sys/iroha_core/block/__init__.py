
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
BlockHeader = make_struct("BlockHeader", [("timestamp", int), ("consensus_estimation", int), ("height", int), ("view_change_index", int), ("previous_block_hash", "iroha_crypto.hash.HashOf"), ("transactions_hash", "iroha_crypto.hash.HashOf"), ("rejected_transactions_hash", "iroha_crypto.hash.HashOf"), ("genesis_topology", "iroha_core.sumeragi.network_topology.Topology")])

CandidateBlock = make_struct("CandidateBlock", [("header", "iroha_core.block.BlockHeader"), ("rejected_transactions", list), ("transactions", list), ("signatures", "iroha_crypto.signature.SignaturesOf"), ("event_recommendations", list)])

CommittedBlock = make_struct("CommittedBlock", [("header", "iroha_core.block.BlockHeader"), ("rejected_transactions", list), ("transactions", list), ("event_recommendations", list), ("signatures", "iroha_crypto.signature.SignaturesOf")])

VersionedCandidateBlock = make_enum("VersionedCandidateBlock", [("V1", get_class("iroha_core.block.CandidateBlock"))], typing.Union[get_class("iroha_core.block.CandidateBlock")])

VersionedCommittedBlock = make_enum("VersionedCommittedBlock", [("V1", get_class("iroha_core.block.CommittedBlock"))], typing.Union[get_class("iroha_core.block.CommittedBlock")])

SelfResolvingTypeVar.resolve_all()
