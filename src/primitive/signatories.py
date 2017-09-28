from src.helper import logger, crypto

class Signatories:
    def __init__(self):
        self.signatories = []

    def append(self, keypair):
        logger.debug("Signatories.append")
        if not filter( lambda signatory : signatory.public_key == keypair.public_key, self.signatories):
            self.signatories.append(keypair)

    def sign(self,tx):
        logger.debug("Signatories.sign")
        payload = tx.payload
        for signatory in self.signatories:
            if not filter( lambda signature : signature.pubkey == signatory.public_key, tx.signatures):
                sign = crypto.sign(signatory, crypto.sign_hash(payload))
                tx.signatures.append(sign)

    def clean(self):
        self.signatories = []
