# Python library for Hyperledger Iroha

This is a source repository for HL Iroha Python library.

Currently, latest 
[HL Iroha release 1.6](https://github.com/hyperledger/iroha/releases) 
is supported. It can be used with one of official docker images:
- `hyperledger/iroha:latest`
- `hyperledger/iroha-burrow:latest` with Hyperledger-Burrow support (smart contracts).

The library works in Python 3 environment (Python 2 is not supported).

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

If you are interested in different HL Iroha client libraries you can check our [Wiki](https://wiki.hyperledger.org/display/iroha/Hyperledger+Iroha).
