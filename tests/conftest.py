import allure
import iroha
import pytest

from tests import client, fake
from tests.helpers import generate_public_key


@pytest.fixture()
def GIVEN_new_domain_id():
    """Fixture to provide a new fake domain id."""
    name = str(len(client.query_all_domains()))+fake.word()
    with allure.step(f'GIVEN a "{name}" name'):
        return name

@pytest.fixture()
def GIVEN_new_account_id(GIVEN_registered_domain):
    """Fixture to provide a new fake account id."""
    name = str(len(client.query_all_accounts())) + fake.word() + '@' + GIVEN_registered_domain
    with allure.step(f'GIVEN a "{name}" name'):
        return name

@pytest.fixture()
def GIVEN_new_asset_id():
    """Fixture to provide a new asset id."""
    asset_name = str(len(client.query_all_assets())) + fake.word()[:3].upper()
    with allure.step(f'GIVEN a "{asset_name}" asset'):
        return asset_name

@pytest.fixture()
def GIVEN_registered_domain(GIVEN_new_domain_id):
    """Fixture to provide registered domain in Iroha"""
    with allure.step(f'GIVEN registered domain name "{GIVEN_new_domain_id}"'):
        (client.submit_executable(
            [iroha.Instruction
             .register_domain(GIVEN_new_domain_id)]))
        return GIVEN_new_domain_id

@pytest.fixture()
def GIVEN_registered_domain_with_registered_accounts(GIVEN_registered_domain, GIVEN_new_account_id):
    """Fixture to provide domain with accounts"""
    with allure.step(
            f'WHEN client registers the account "{GIVEN_new_account_id}"'):
        (client.submit_executable(
            [iroha.Instruction
             .register_account(
                GIVEN_new_account_id,
                [generate_public_key(seed="abcd1122")])]))
        return GIVEN_registered_domain