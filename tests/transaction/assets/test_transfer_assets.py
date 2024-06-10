import allure
import iroha

import pytest

from tests import client

@pytest.fixture(scope="function", autouse=True)
def story_account_transfer_asset():
    allure.dynamic.story("Account transfers assets")

@allure.label("sdk_test_id", "transfer_asset")
@pytest.mark.xfail(reason="https://github.com/hyperledger/iroha-python/issues/205")
def test_transfer_asset(
    GIVEN_minted_asset,
    GIVEN_registered_account):
    with allure.step(
            f'WHEN client transfers an asset'):
        (client.submit_executable_only_success(
            [iroha.Instruction.
            transfer(
                5,
                GIVEN_minted_asset,
                GIVEN_registered_account)]))
    with allure.step(
            f'THEN another account should have assets'):
        assert client.query_all_assets()
