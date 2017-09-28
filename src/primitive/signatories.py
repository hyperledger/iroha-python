from src.helper import logger, crypto

from schema.primitive_pb2 import Signature

class Signatories:
    def __init__(self):
        self.signatories = []

    def append(self, keypair):
        logger.debug("Signatories.append")
        if len(list(filter( lambda signatory : signatory.public_key == keypair.public_key, self.signatories))) == 0:
            self.signatories.append(keypair)

    def sign(self,tx):
        logger.debug("Signatories.sign")
        payload = tx.payload
        for signatory in self.signatories:
            if len(list(filter( lambda signature : signature.pubkey == signatory.public_key, tx.signatures))) == 0:
                sign = Signature(
                    pubkey = signatory.public_key,
                    signature = crypto.sign(signatory, crypto.sign_hash(payload))
                )
                tx.signatures.extend([sign])

    def clean(self):
        self.signatories = []

    def size(self):
        return len(self.signatories)
