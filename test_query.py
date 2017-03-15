
from iroha import Kannagi
from transaction import TransactionBuilder

from protos.api_pb2 import Asset,BaseObject,Query

k = Kannagi()
publicKey = "2H8I8xrtXvPtyvT44L9QI1QTlFIUEl3JVArpFbyvGg8="
iori      = "m6G6apYkfCCRZros4oN4voMzCfADI4JmbPMhnkUVd0I="
mizuki    = "tuIWczwegKNqgpohuAcMp1ZBl3Qr0igAgG1CiZMhRX0="

print(k.get_all_transation())

print("=====================")

print(k.get_asset_info( mizuki, "mizuki"))
print(k.get_asset_info( iori, "mizuki"))


