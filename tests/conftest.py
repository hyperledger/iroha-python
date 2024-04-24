import re
import time

import allure
import iroha
import pytest

from tests import client, fake
from tests.helpers import generate_public_key

# Fixtures for Generating New Identifiers
@pytest.fixture()
def GIVEN_new_domain_id():
    """Fixture to provide a new fake domain id."""
    name = fake.country().split()[0] + str(len(client.query_all_domains()))
    with allure.step(f'GIVEN a "{name}" name'):
        return name

@pytest.fixture()
def GIVEN_new_account_id(GIVEN_registered_domain):
    """Fixture to provide a new fake account id."""
    name = fake.first_name() + str(len(client.query_all_accounts())) + '@' + GIVEN_registered_domain
    with allure.step(f'GIVEN a "{name}" name'):
        return name

@pytest.fixture()
def GIVEN_new_asset_id():
    """Fixture to provide a new asset id."""
    asset_name = fake.word()[:3].upper() + str(len(client.query_all_asset_definitions()))
    with allure.step(f'GIVEN a "{asset_name}" asset'):
        return asset_name

@pytest.fixture()
def GIVEN_new_asset_definition_id(GIVEN_new_asset_id, GIVEN_registered_domain):
    """Fixture to provide a new asset definition id."""
    asset_name = GIVEN_new_asset_id + "#" + GIVEN_registered_domain
    with allure.step(f'GIVEN a "{asset_name}" asset'):
        return asset_name

# Fixtures for Registering Entities
@pytest.fixture()
def GIVEN_registered_asset_definition(GIVEN_new_asset_definition_id):
    """Fixture to provide a registered asset definition."""
    with allure.step(
            f'GIVEN registered asset definition "{GIVEN_new_asset_definition_id}"'):
        (client.submit_executable(
            [iroha.Instruction
            .register_asset_definition(
                GIVEN_new_asset_definition_id,
                "Quantity")]))
        time.sleep(2)
        return GIVEN_new_asset_definition_id

@pytest.fixture()
def GIVEN_registered_domain(GIVEN_new_domain_id):
    """Fixture to provide a registered domain in Iroha"""
    with allure.step(f'GIVEN registered domain name "{GIVEN_new_domain_id}"'):
        (client.submit_executable(
            [iroha.Instruction
             .register_domain(GIVEN_new_domain_id)]))
        time.sleep(2)
        return GIVEN_new_domain_id

@pytest.fixture()
def GIVEN_registered_account(GIVEN_new_account_id):
    """Fixture to provide a registered account"""
    with allure.step(
            f'GIVEN client registered the account "{GIVEN_new_account_id}"'):
        (client.submit_executable(
            [iroha.Instruction
             .register_account(
                GIVEN_new_account_id,
                [generate_public_key(seed="abcd1122")])]))
        time.sleep(2)
        return GIVEN_new_account_id

@pytest.fixture()
def GIVEN_registered_domain_with_registered_accounts(
        GIVEN_registered_domain,
        GIVEN_new_account_id):
    """Fixture to provide a domain with accounts"""
    with allure.step(
            f'GIVEN client registers the account "{GIVEN_new_account_id}"'):
        (client.submit_executable(
            [iroha.Instruction
             .register_account(
                GIVEN_new_account_id,
                [generate_public_key(seed="abcd1122")])]))
        time.sleep(2)
        return GIVEN_registered_domain

@pytest.fixture()
def GIVEN_registered_account_with_minted_assets(
        GIVEN_registered_asset_definition,
        GIVEN_registered_account
):
    """Fixture to provide an account with minted assets"""
    asset = (lambda s: re.sub(r'(\b\w+\b)(?=.*\1)', '', s))(
        GIVEN_registered_asset_definition + '#' + GIVEN_registered_account)
    with allure.step(
            f'WHEN client mints an asset "{asset}"'):
        (client.submit_executable(
            [iroha.Instruction
            .mint_asset(
                5,
                asset,
                "Quantity")]))
    time.sleep(3)
    return GIVEN_registered_account
