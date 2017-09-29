from src.helper import logger, crypto

from schema.primitive_pb2 import Signature

class Signatories:
    def __init__(self):
        self.signatories = []

    def append(self, keypair):
        logger.debug("Signatories.append")
        if not [ signatory for signatory in self.signatories if signatory.public_key == keypair.public_key ]:
            self.signatories.append(keypair)

    def sign(self,tx):
        logger.debug("Signatories.sign")
        payload = tx.payload
        for signatory in self.signatories:
            if not [ signature for signature in tx.signatures if signature.pubkey == signatory.public_key ]:
                tx.signatures.extend([
                    Signature(
                        pubkey = signatory.public_key,
                        signature = crypto.sign(signatory, crypto.sign_hash(payload))
                    )
                ])

    def clean(self):
        self.signatories = []

    def size(self):
        return len(self.signatories)
