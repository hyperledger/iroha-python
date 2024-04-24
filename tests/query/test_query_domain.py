import allure
import pytest

from tests import client

@pytest.fixture(scope="function", autouse=True)
def story_account_queries_domains():
    allure.dynamic.story("Account queries domains")
    allure.dynamic.label("permission", "no_permission_required")

@allure.label("sdk_test_id", "query_all_domains")
def test_query_all_domains():
    with allure.step('WHEN client queries all domains'):
        all_domains = client.query_all_domains()
    with allure.step('THEN there should be some accounts present'):
        assert len(all_domains) > 0, "No domains found in the system"