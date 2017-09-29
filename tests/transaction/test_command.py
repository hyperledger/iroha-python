import unittest

from src.helper import logger,crypto
from src.helper.amount import int2amount
from src.transaction.command import wrap_cmd
from schema.commands_pb2 import Command

class CommandTest(unittest.TestCase):
    def setUp(self):
        logger.setDebug()
        logger.debug("CommandTest")
        self.keypair = crypto.create_key_pair()

    def test_wrap_cmd_create_account(self):
        create_ac = Command(
            create_account = Command.CreateAccount(
                account_name = "rihito",
                domain_id = "light.wing",
                main_pubkey = self.keypair.public_key
            )
        )
        self.assertEqual(create_ac,wrap_cmd(create_ac.create_account))


    def test_wrap_cmd_add_signatory(self):
        add_sig = Command(
            add_signatory = Command.AddSignatory(
                account_id = "rihito@light.wing",
                pubkey = self.keypair.public_key
            )
        )
        self.assertEqual(add_sig,wrap_cmd(add_sig.add_signatory))

    def test_wrap_cmd_set_account_quorum(self):
        set_ac_q = Command(
            set_account_quorum = Command.SetAccountQuorum(
                account_id = "rihito@light.wing",
                quorum = 100
            )
        )
        self.assertEqual(set_ac_q, wrap_cmd(set_ac_q.set_account_quorum))

    def test_wrap_cmd_create_domain(self):
        create_d = Command(
            create_domain = Command.CreateDomain(
                domain_name="ichigo.mashimaro"
            )
        )
        self.assertEqual(create_d, wrap_cmd(create_d.create_domain))

    def test_wrap_cmd_create_asset(self):
        create_as = Command(
            create_asset = Command.CreateAsset(
                asset_name="yen",
                domain_id="ichigo.mashimaro",
                precision=3
            )
        )
        self.assertEqual(create_as, wrap_cmd(create_as.create_asset))

    def test_wrap_cmd_add_asset_quantity(self):
        add_asset_q = Command(
            add_asset_quantity = Command.AddAssetQuantity(
                account_id="chika@ichigo.mashimaro",
                asset_id="ichigo.mashimaro/yen",
                amount=int2amount(100)
            )
        )
        self.assertEqual(add_asset_q, wrap_cmd(add_asset_q.add_asset_quantity))

    def test_wrap_cmd_transfer_asset(self):
        transfer_as = Command(
            transfer_asset = Command.TransferAsset(
                src_account_id="chika@ichigo.mashimaro",
                dest_account_id="miu@ichigo.mashimaro",
                asset_id="ichigo.mashimaro/yen",
                amount=int2amount(100)
            )
        )
        self.assertEqual(transfer_as,wrap_cmd(transfer_as.transfer_asset))
