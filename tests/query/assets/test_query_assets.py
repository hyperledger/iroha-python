import allure

from tests import client


@allure.id("2381")
@allure.label("sdk_test_id", "query_all_assets_owned_by_account")
def test_query_all_assets_owned_by_account(
        GIVEN_registered_account_with_minted_assets):
    with allure.step(
            f'WHEN client queries all assets owned by account "{GIVEN_registered_account_with_minted_assets}"'):
        assets_owned_by_account = client.query_all_assets_owned_by_account(GIVEN_registered_account_with_minted_assets)
    with allure.step(
            f'THEN the response should be a non-empty list of assets owned by account "{GIVEN_registered_account_with_minted_assets}"'):
        assert isinstance(assets_owned_by_account, list) and assets_owned_by_account, \
            f"Expected a non-empty list of assets owned by account {GIVEN_registered_account_with_minted_assets}, got {assets_owned_by_account}"


@allure.id("2380")
@allure.label("sdk_test_id", "query_all_assets")
def test_query_all_assets(
        GIVEN_registered_account_with_minted_assets):
    with allure.step(
            f'WHEN client queries all assets'):
        assets_owned_by_account = client.query_all_assets()
    with allure.step(
            f'THEN the response should be a non-empty list of assets "{GIVEN_registered_account_with_minted_assets}"'):
        assert isinstance(assets_owned_by_account, list) and assets_owned_by_account, \
            f"Expected a non-empty list of assets {GIVEN_registered_account_with_minted_assets}, got {assets_owned_by_account}"
