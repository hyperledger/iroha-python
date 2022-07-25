from ....rust import Enum, make_struct, make_tuple, Dict
BlockPublisherMessage = Enum[("SubscriptionAccepted", type(None)), ("Block", "iroha_core.block.VersionedCommittedBlock")] 
BlockSubscriberMessage = Enum[("SubscriptionRequest", int), ("BlockReceived", type(None))] 
VersionedBlockPublisherMessage = Enum[("V1", "iroha_core.block.stream.BlockPublisherMessage")] 
VersionedBlockSubscriberMessage = Enum[("V1", "iroha_core.block.stream.BlockSubscriberMessage")] 
