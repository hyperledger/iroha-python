import allure
import iroha
import time
import pytest

from tests import client
from tests.helpers import generate_public_key

@pytest.fixture(scope="function", autouse=True)
def story_account_register_account():
    allure.dynamic.story("Account registers an account")
    allure.dynamic.label("permission", "no_permission_required")

@allure.label("sdk_test_id", "register_account")
def test_register_account(
        GIVEN_new_account_id):
    with allure.step(
            f'WHEN client registers the account "{GIVEN_new_account_id}"'):
        (client.submit_executable(
            [iroha.Instruction
             .register_account(
                GIVEN_new_account_id,
                [generate_public_key(seed="abcd1122")])]))
        time.sleep(3)
    with allure.step(
            f'THEN Iroha should have the "{GIVEN_new_account_id}" account'):
        assert GIVEN_new_account_id in client.query_all_accounts()