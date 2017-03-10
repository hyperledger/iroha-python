import iroha
from iroha import Kannagi
from transaction import TransactionBuilder

# ToDo I should make builder...
from protos.api_pb2 import Account,Asset,BaseObject,Query

k = Kannagi()
publicKey = iroha.KeyPair().public_key

# This sample is bad. so we should create builder
account = Account(
    publicKey=publicKey,
    name="mizuki",
    assets = [
        "iroha"
    ]
)
tx = TransactionBuilder("add", publicKey).set_account(account).build()
k.torii(tx)

query = Query(
    senderPubkey = publicKey,
    type="account",
    value = {
    "name": BaseObject(valueString="mizuki")
})

print(k.assetRepository(query))
