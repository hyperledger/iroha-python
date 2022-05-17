from ......rust import Enum, Struct, Tuple, Dict
PeerEvent = Enum[("Added", "iroha_data_model.peer.Id"), ("Removed", "iroha_data_model.peer.Id")] 
