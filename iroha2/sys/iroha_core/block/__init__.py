from ...rust import Enum, Struct, Tuple, Dict
BlockHeader = Struct[("timestamp", int), ("consensus_estimation", int), ("height", int), ("previous_block_hash", "iroha_crypto.hash.HashOf"), ("transactions_hash", "iroha_crypto.hash.HashOf"), ("rejected_transactions_hash", "iroha_crypto.hash.HashOf"), ("view_change_proofs", "iroha_core.sumeragi.view_change.ProofChain"), ("invalidated_blocks_hashes", list), ("genesis_topology", "iroha_core.sumeragi.network_topology.Topology")]

CommittedBlock = Struct[("header", "iroha_core.block.BlockHeader"), ("rejected_transactions", list), ("transactions", list), ("event_recommendations", list), ("signatures", "iroha_crypto.signature.SignaturesOf")]

ValidBlock = Struct[("header", "iroha_core.block.BlockHeader"), ("rejected_transactions", list), ("transactions", list), ("signatures", list), ("event_recommendations", list)]

VersionedCommittedBlock = Enum[("V1", "iroha_core.block.CommittedBlock")] 
VersionedValidBlock = Enum[("V1", "iroha_core.block.ValidBlock")] 
