# Python library for Hyperledger Iroha


This is a source repository for HL Iroha Python library.

Currently, latest HL Iroha rc5 release (`hyperledger/iroha:latest` Docker image) is supported.

The library works in Python 3 environment (Python 2 is not supported now).

### Installation

```bash
pip install iroha
```


### Usage Example

```python
from iroha import Iroha, IrohaCrypto, IrohaGrpc

iroha = Iroha('alice@test')
net = IrohaGrpc('127.0.0.1:50051')

alice_key = IrohaCrypto.private_key()
alice_tx = iroha.transaction(
    [iroha.command(
        'TransferAsset', 
        src_account_id='alice@test', 
        dest_account_id='bob@test', 
        asset_id='bitcoin#test',
        description='test',
        amount='1'
    )]
)
IrohaCrypto.sign_transaction(alice_tx, alice_key)
net.send_tx(alice_tx)

for status in net.tx_status_stream(alice_tx):
    print(status)
```

Please explore [examples](examples) directory for more usage examples.

All the library methods have docstrings in its source [iroha.py](iroha/iroha.py).

*The links above are broken outside the [hyperledger/iroha-python](https://github.com/hyperledger/iroha-python) GitHub repository.*
