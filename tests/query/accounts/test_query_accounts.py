import allure

from tests import client


@allure.id("2378")
@allure.label("sdk_test_id", "query_all_accounts")
def test_query_all_accounts():
    with allure.step('WHEN client queries all accounts'):
        all_accounts = client.query_all_accounts()
    with allure.step('THEN there should be some accounts present'):
        assert len(all_accounts) > 0, "No accounts found in the system"


@allure.id("2378")
@allure.label("sdk_test_id", "query_all_accounts_in_domain")
def test_query_all_accounts_in_domain(
        GIVEN_registered_domain_with_registered_accounts):
    with allure.step(
            f'WHEN client queries all accounts in domain "{GIVEN_registered_domain_with_registered_accounts}"'):
        accounts_in_domain = client.query_all_accounts_in_domain(GIVEN_registered_domain_with_registered_accounts)
    with allure.step(
            f'THEN the response should be a non-empty list of accounts in domain "{GIVEN_registered_domain_with_registered_accounts}"'):
        assert isinstance(accounts_in_domain, list) and accounts_in_domain, \
            f"Expected a non-empty list of accounts in the domain {GIVEN_registered_domain_with_registered_accounts}, got {accounts_in_domain}"
