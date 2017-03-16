import iroha
from iroha import Kannagi
from transaction import TransactionBuilder

# ToDo I should make builder...
from protos.api_pb2 import Account,Asset,BaseObject,Query

k = Kannagi()
publicKey = iroha.create_key_pair().public_key

iori = "m6G6apYkfCCRZros4oN4voMzCfADI4JmbPMhnkUVd0I="
mizuki = "tuIWczwegKNqgpohuAcMp1ZBl3Qr0igAgG1CiZMhRX0="
# This sample is bad. so we should create builder
asset = Asset(
    domain="sample",
    name="mizuki",
    value = {
       "targetName": BaseObject( valueString = "Iori1"),
       "Iori1": BaseObject( valueInt = 1)
    }
)
tx = TransactionBuilder("transfer", iori, mizuki).set_asset(asset).build()
k.torii(tx)

print(k.get_account_info(iori))
