import json
from schema.transaction_pb2 import Transaction
from schema.commands_pb2 import Command
from schema.primitive_pb2 import Amount
from src.helper import crypto, logger

def getGenesisTransaction(path):
    logger.info("getGenesisTransaction")
    f = open(path)
    js = json.loads(f.read())
    f.close()

    try:
        cmds = []
        for command in js["commands"]:
            if command["command_type"] == "create_account":
                cmds.append(Command(
                    create_account = Command.CreateAccount(
                        account_name = command["account_name"],
                        domain_id = command["domain_id"],
                        main_pubkey = command["main_pubkey"].encode()
                    )
                ))
            elif command["command_type"] == "add_signatory":
                cmds.append(Command(
                    add_signatory = Command.AddSignatory(
                        account_id = command["account_id"],
                        pubkey = command["pubkey"].encode()
                    )
                ))
            elif command["command_type"] == "remove_signatory":
                cmds.append(Command(
                    remove_signatory = Command.RemoveSignatory(
                        account_id = command["account_id"],
                        pubkey = command["pubkey"].encode()
                    )
                ))
            elif command["command_type"] == "set_account_quorum":
                cmds.append(Command(
                    set_account_quorum = Command.SetAccountQuorum(
                        account_id = command["account_id"],
                        quorum = command["quorum"]
                    )
                ))

            elif command["command_type"] == "create_domain":
                cmds.append(Command(
                    create_domain = Command.CreateDomain(
                        domain_name = command["domain_name"]
                    )
                ))

            elif command["command_type"] == "create_asset":
                cmds.append(Command(
                    create_asset = Command.CreateAsset(
                        asset_name = command["asset_name"],
                        domain_id = command["domain_id"],
                        precision = command["precision"]
                    )
                ))

            elif command["command_type"] == "add_asset_quantity":
                cmds.append(Command(
                    add_asset_quantity = Command.AddAssetQuantity(
                        account_id = command["account_id"],
                        asset_id = command["asset_id"],
                        amount = Amount(
                            integer_part = command["amount"]["integer_part"],
                            fractial_part = command["amount"]["fractial_part"]
                        )
                    )
                ))

            elif command["command_type"] == "transfer_asset":
                cmds.append(Command(
                    transfer_asset = Command.TransferAsset(
                        src_account_id = command["src_account_id"],
                        dest_account_id = command["dest_account_id"],
                        asset_id = command["asset_id"],
                        amount=Amount(
                            integer_part=command["amount"]["integer_part"],
                            fractial_part=command["amount"]["fractial_part"]
                        )
                    )
                ))

        tx = Transaction(
            payload = Transaction.Payload(
                commands = cmds,
                creator_account_id = "admin@root",
                tx_counter = 0,
                created_time = crypto.now()
            ),
            signature = []
        )
    except:
        logger.info("Genesis parse Exception")
        return Transaction(
            payload = Transaction.Payload(
                commands = [],
                creator_account_id = "admin@root",
                tx_counter = 0,
                created_time = crypto.now()
            ),
            signature = []
        )

    logger.debug(tx)
    logger.info("Correct Genesis Parse")

    return tx
