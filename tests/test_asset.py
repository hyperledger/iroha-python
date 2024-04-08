import allure
import iroha
import time

import pytest

from tests import client

@pytest.fixture(scope="function", autouse=True)
def story_account_register_asset():
    allure.dynamic.story("Account registers an asset")
    allure.dynamic.label("permission", "no_permission_required")

def test_register_asset(
        GIVEN_new_asset_id):
    assets = client.query_all_assets_owned_by_account("alice@wonderland")

    asset_definition_id = "time_" + str(len(assets)) + "#wonderland"
    asset_id = "time_" + str(len(assets)) + "##alice@wonderland"
    assert asset_id not in assets
    
    register_definition = iroha.Instruction.register_asset_definition(asset_definition_id, "Quantity")
    
    mint = iroha.Instruction.mint_asset(5, asset_id, "Quantity")
    
    client.submit_executable([register_definition, mint])

    for x in range(30):
        assets = client.query_all_assets_owned_by_account("alice@wonderland")
        
        if asset_id in assets:
            break
        
        time.sleep(1)
        
    
    assert asset_id in assets
    