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
