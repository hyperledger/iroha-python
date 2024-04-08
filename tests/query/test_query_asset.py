import allure
import time
import pytest

from tests import client

@pytest.fixture(scope="function", autouse=True)
def story_account_register_account():
    allure.dynamic.story("Account queries assets")
    allure.dynamic.label("permission", "no_permission_required")

@pytest.mark.xfail(reason="TO DO")
@allure.label("sdk_test_id", "query_all_assets_owned_by_account")
def test_query_all_assets_owned_by_account(
        GIVEN_registered_account_with_assets):
    with allure.step(
            f'WHEN client queries all assets owned by account "{GIVEN_registered_account_with_assets}"'):
        time.sleep(3)
        assets_owned_by_account = client.query_all_assets_owned_by_account(GIVEN_registered_account_with_assets)
    with allure.step(
            f'THEN the response should be a non-empty list of assets owned by account "{GIVEN_registered_account_with_assets}"'):
        assert isinstance(assets_owned_by_account, list) and assets_owned_by_account, \
            f"Expected a non-empty list of assets owned by account {GIVEN_registered_account_with_assets}, got {assets_owned_by_account}"

    