from __future__ import print_function

import re

from iroha.helper import crypto, logger
from iroha.primitive.amount import amount2int

MAX_DELAY = 1000 * 3600 * 24  # max-delay between tx creation and validation

ACCOUNT_NAME = re.compile(r"^[a-z_0-9]{1,32}$")
ACCOUNT_ID = re.compile(r"^[a-z_0-9]{1,32}\@[a-z_0-9]{1,32}(\.[a-z_0-9]{1,32}){0,4}$")
DOMAIN_ID = re.compile(r"^[a-z_0-9]{1,32}(\.[a-z_0-9]{1,32}){0,4}$")
ASSET_NAME = re.compile(r"^[a-z_0-9]{1,32}$")
ASSET_ID = re.compile(r"^[a-z_0-9]{1,32}(\.[a-z_0-9]{1,32}){0,4}\/[a-z_0-9]{1,32}$")
PEER_IP = re.compile(r"^[0-9]{1,3}(\.[0-9]{1,3}){3}$")


def command(cmd):
    logger.info(cmd.HasField)
    if cmd.HasField("create_account"):
        return create_account(cmd.create_account)
    elif cmd.HasField("add_signatory"):
        return add_signatory(cmd.add_signatory)
    elif cmd.HasField("remove_signatory"):
        return remove_signatory(cmd.remove_signatory)
    elif cmd.HasField("set_account_quorum"):
        return set_account_quorum(cmd.set_account_quorum)
    elif cmd.HasField("create_domain"):
        return create_domain(cmd.create_domain)
    elif cmd.HasField("create_asset"):
        return create_asset(cmd.create_asset)
    elif cmd.HasField("add_asset_quantity"):
        return add_asset_quantity(cmd.add_asset_quantity)
    elif cmd.HasField("transfer_asset"):
        return transfer_asset(cmd.transfer_asset)
    logger.info("Stateless validate Not has field")
    return False

def verify(transaction):
    logger.info("Transaction Stateless Verify")
    payload = transaction.payload
    for cmd in transaction.payload.commands:
        if not command(cmd):
            logger.info("Stateless Command Failed")
            return False

    for signature in transaction.signatures:
        if not crypto.verify(signature.pubkey,
                             signature.signature,
                             crypto.sign_hash(payload)):
            logger.info("Stateless Signature Verify Failed")
            return False

    if verify_created_time(payload.created_time):
        return True
    return False



def create_account(cmd):
    logger.info("stateless validate create_account")
    if verify_account_name(cmd.account_name) and verify_domain_id(cmd.domain_id) and verify_pubkey(cmd.main_pubkey):
        return True
    return False

def add_signatory(cmd):
    logger.info("stateless validate add_signatory")
    if verify_account_id(cmd.account_id) and verify_pubkey(cmd.pubkey):
        return True
    return False

def remove_signatory(cmd):
    logger.info("stateless validate remove_signaotry")
    if verify_account_id(cmd.account_id) and verify_pubkey(cmd.pubkey):
        return True
    return False

def set_account_quorum(cmd):
    logger.info("stateless validate set_account_quorum")
    if verify_account_id(cmd.account_id) and verify_quorum(cmd.quorum):
        return True
    return False

def create_domain(cmd):
    logger.info("stateless validate create_domain")
    if verify_domain_id(cmd.domain_name):
        return True
    return False

def create_asset(cmd):
    logger.info("stateless validate create_asset")
    if verify_asset_name(cmd.asset_name) and verify_domain_id(cmd.domain_id):
        return True
    return False

def add_asset_quantity(cmd):
    logger.info("stateless validate add_asset_quantity")
    if verify_asset_id(cmd.asset_id) and verify_account_id(cmd.account_id) and verify_amount(cmd.amount):
        return True
    return False

def transfer_asset(cmd):
    logger.info("stateless validate transfer_asset")
    if verify_asset_id(cmd.asset_id) and verify_account_id(cmd.src_account_id) and verify_account_id(cmd.dest_account_id) and verify_amount(cmd.amount):
        return True
    return False





def query(qry):
    logger.info("Query Stateless Validator")
    payload = qry.payload

    if not verify_account_id(payload.creator_account_id):
        return False
    if not verify_created_time(payload.created_time):
        return False

    # TODO not deceided query signatures
    '''
    for signature in qry.signature:
        if not crypto.verify(signature.pubkey,
                             signature.signature,
                             crypto.sign_hash(payload)):
            logger.info("Stateless Signature Verify Failed")
            return False
    '''

    if payload.HasField("get_account"):
        return get_account(payload.get_account)
    elif payload.HasField("get_signatories"):
        return get_signatories(payload.get_signatories)
    elif payload.HasField("get_account_transactions"):
        return get_account_transactions(payload.get_account_transactions)
    elif payload.HasField("get_account_asset_transactions"):
        return get_account_asset_transactions(payload.get_account_asset_transactions)
    elif payload.HasField("get_account_assets"):
        return get_account_assets(payload.get_account_assets)
    elif payload.HasField("get_transactions"):
        return get_transactions(payload.get_transactions)
    logger.info("Stateless validate Not has field")
    return False



def get_account(req):
    logger.info("stateless validate get_account")
    if verify_account_id(req.account_id):
        return True
    return False

def get_signatories(req):
    logger.info("stateless validate get_signatories")
    if verify_account_id(req.account_id):
        return True
    return False

def get_account_transactions(req):
    logger.info("stateless validate get_account_transactions")
    if verify_account_id(req.account_id):
        return True
    return False

def get_account_asset_transactions(req):
    logger.info("stateless validate get_account_asset_transactions")
    # asset_id は""を許す
    if verify_account_id(req.account_id):
        return True
    return False

def get_account_assets(req):
    logger.info("stateless validate get_account_assets")
    if verify_account_id(req.account_id) and verify_asset_id(req.asset_id):
        return True
    return False


def get_transactions(req):
    logger.info("statless validate get_transactions")
    for hash in req.tx_hashes:
        if len(hash) != 32:
            return False
    return True




def verify_created_time(time):
    logger.info("Stateless Check Time")
    logger.info("created time: " + str(time))
    now = crypto.now()
    logger.info("now time    : " + str(now))
    one_second = 1000
    # なんか時間ずれるの5秒ほど許容する。
    if now - MAX_DELAY <= time and time <= now + one_second * 5:
        return True
    logger.info("Stateless Out Range Time Failed")
    return False

def verify_account_name(account_name):
    if ACCOUNT_NAME.match(account_name) is None:
        logger.info("Stateless Account Name Failed: " + account_name)
        return False
    return True

def verify_account_id(account_id):
    if ACCOUNT_ID.match(account_id) is None:
        logger.info("Stateless Account Id Failed: " + account_id)
        return False
    return True

def verify_domain_id(domain_id):
    if DOMAIN_ID.match(domain_id) is None:
        logger.info("Stateless Domain Id Failed: " + domain_id)
        return False
    return True


def verify_asset_name(asset_name):
    if ASSET_NAME.match(asset_name) is None:
        logger.info("Stateless Asset Name Failed: " + asset_name)
        return False
    return True

def verify_asset_id(asset_id):
    if ASSET_ID.match(asset_id) is None:
        logger.info("Stateless Asset Id Failed: " + asset_id)
        return False
    return True

def verify_pubkey(pubkey):
    try:
        key = crypto.b64decode(pubkey)
    except:
        logger.info("Stateless Public Key not Base64 Encode")
        return False
    if len(key) == 32:
        return True
    logger.info("Stateless Public Key Length Failed: " + key.decode())
    return False


def verify_quorum(quorum):
    if 0 != quorum:
        return True
    logger.info("Stateless Quorum Failed: " + str(quorum))
    return False

def verify_amount(amount):
    if amount2int(amount) == 0:
        logger.warning("Stateless Amount 0 Error")
        return False
    return True


def verify_ip(peer_ip):
    if PEER_IP.match(peer_ip) is None:
        logger.info("Stateless Peer Ip Failed: " + peer_ip)
        return False
    return True

def verify_port(peer_port):
    if 0 <= peer_port and peer_port <= 65535:
        return True
    return False
