
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
BlockHeader = make_struct("BlockHeader", [("timestamp", int), ("consensus_estimation", int), ("height", int), ("view_change_index", int), ("previous_block_hash", "iroha_crypto.hash.HashOf"), ("transactions_hash", "iroha_crypto.hash.HashOf"), ("rejected_transactions_hash", "iroha_crypto.hash.HashOf"), ("committed_with_topology", list)])

SelfResolvingTypeVar.resolve_all()
