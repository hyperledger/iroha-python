
from connection import Kannagi
from transaction import TransactionBuilder

from protos.api_pb2 import Asset,BaseObject,Query

k = Kannagi()
publicKey = "GXQ/Gc2Ru3NLKiJ2mqC+ApG2sUWuG/jHJ6joAkuRe+s="
# This sample is bad. so we should create builder
asset = Asset(
    domain="sample",
    name="mizuki",
    value = {
        "sample": BaseObject(valueString="Nao")
    },
)
tx = TransactionBuilder("add", publicKey).set_asset(asset).build()
k.torii(tx)

query = Query(
    type="asset",
    value = {
    "name": BaseObject(valueString="mizuki")
})

print(k.assetRepository(query))
