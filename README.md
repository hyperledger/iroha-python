# iroha-python [![CircleCI](https://img.shields.io/circleci/project/github/hyperledger/iroha-python/master.svg)](https://circleci.com/gh/hyperledger/iroha-python/tree/master)

Python library for [Hyperledger Iroha](https://github.com/hyperledger/iroha).

## Install

### Python

Supported Python versions: 3.6 (see `tox.ini`). ( WIP : not tried 2.x )
Multiple Python versions can be installed with your system package manager or with the [pyenv](https://github.com/pyenv/pyenv) tool.
The pyenv itself can also be installed with a system package manager or with the [pyenv-installer](https://github.com/pyenv/pyenv-installer) script.

#### Example installation steps

```sh
# Install pyenv using pyenv-installer
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
# pyenv initialization
export PATH="${HOME}/.pyenv/bin:${PATH}"
eval "$(pyenv init -)"
# Also initialize on startup; if you are using zsh, replace "~/.bashrc" with "~/.zshrc"
echo 'export PATH="${HOME}/.pyenv/bin:${PATH}"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# Install the most recent Python versions (both 3 and 2)
pyenv install 3.6.0
pyenv install 2.7.13
# Bring both installed versions into the scope: we are testing against both versions
pyenv global 3.6.0 2.7.13
# Only the "tox" package needs to be installed manually
pip install tox
```

## How to use
### Install
```
$ cd iroha-python
$ pip install -r requirement.txt
$ make all
$ python setup.py install
```

### Example Code
```python
import time
import iroha

iroha.setDebugLog()

# Generate Connection used to connect iroha
connection = iroha.gen_connection(ip="127.0.0.1",port=50051)
#connection = iroha.gen_connection(ip="0.0.0.0",port="10001")
creator = "sioya@sporting.salt"
tx_counter = 0

# Generate Keypairs ( Signatories )
keypairs = []
keypairs.append(iroha.keygen())
keypairs.append(iroha.keygen())


# Generate Creator creating transaction and query
creator = iroha.gen_creator("sinkai@jump.com",keypairs,connection)

# Create Transaction
tx1 = creator.create_tx()

# Add Commmand to tx1
tx1.add_command(
    iroha.CreateAccount(
        account_name = "sinkai",
        domain_id = "jump.com",
        main_pubkey = keypairs[0].public_key,
    )
)

# Sign Transaction
tx1.sign()

# Verify tx1 Transaction
assert(tx1.verify())

# Issue tx1 Transaction
tx1.issue()

# Check tranaction status from iroha
while tx1.check().tx_status == iroha.TxStatus.Value("ON_PROCESS"):
    print("Wait Commit")
    time.sleep(0.1)


# Create Query
query1 = creator.create_query()

# Set Query to query1
query1.set_request(
    iroha.GetAccount(
        account_id = "sinkai@jump.com"
    )
)

# Verify query1 Query
assert(query1.verify())

# Issue query1 Query and Get Response
ret = query1.issue()

# Handling query response
if ret.verify():
    if ret.has_error():
        print( ret.error_response() )
    elif ret.has_account():
        print( ret.account() )
    else:
        assert(False)
else:
    print("unverified")
    assert(False)

```

### test
```
$ tox
```
