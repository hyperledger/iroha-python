from schema.commands_pb2 import Command
from iroha.helper import logger

def wrap_cmd(cmd):
    if type(cmd) == type(Command.CreateAccount()):
        return Command(create_account = cmd)
    elif type(cmd) == type(Command.AddSignatory()):
        return Command(add_signatory = cmd)
    elif type(cmd) == type(Command.RemoveSignatory()):
        return Command(remove_signaotory = cmd)
    elif type(cmd) == type(Command.SetAccountQuorum()):
        return Command(set_account_quorum = cmd)
    elif type(cmd) == type(Command.CreateAsset()):
        return Command(create_asset = cmd)
    elif type(cmd) == type(Command.CreateDomain()):
        return Command(create_domain = cmd)
    elif type(cmd) == type(Command.AddAssetQuantity()):
        return Command(add_asset_quantity = cmd)
    elif type(cmd) == type(Command.TransferAsset()):
        return Command(transfer_asset = cmd)
    # TODO throw except
    logger.warning("Not Command Type")
    return False
