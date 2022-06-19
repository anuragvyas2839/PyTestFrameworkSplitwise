import logging
import pytest
from unittest.mock import patch

from services.create_mock_entities import MockBalances, MockRequestResponse
from utils import request_utils
from test_data import mock_transactions, mock_balances


@pytest.fixture(autouse=True, scope='class')
def setup() -> None:
    '''Setup urls needed in the test class'''
    global url_post_transaction, url_balance
    url_post_transaction = request_utils.get_endpoint_url('transaction')
    url_balance = request_utils.get_endpoint_url('balance')


@pytest.fixture(autouse=True, scope='class')
def mock_transactions_and_balances() -> None:
    '''Get mock entities needed in the test class'''
    global mock_post_new_resource_request_response, mock_balances_for_4_users_transactions
    mock_post_new_resource_request_response = MockRequestResponse(status_code=201)
    mock_balances = MockBalances()
    mock_balances_for_4_users_transactions = mock_balances.get_mock_balances_user2_user1_owe_user4_user3()


@pytest.fixture(autouse=True, scope='class')
def post_request_params() -> None:
    '''Create params needed for api calls in the test class'''
    global params_for_post_transaction_equal_split, params_for_post_transaction_unequal_split, params_for_balances
    transaction_equal_split = mock_transactions.transaction_with_4_users_equal_split
    params_for_post_transaction_equal_split = {'gpin': transaction_equal_split['gpin'],
                                               'user_to_amount_map': transaction_equal_split['user_to_amount_map'],
                                               'transaction_name': transaction_equal_split['transaction_name']}
    transaction_unequal_split = mock_transactions.transaction_with_4_users_unequal_split
    params_for_post_transaction_unequal_split = {'gpin': transaction_unequal_split['gpin'],
                                                 'user_to_amount_map': transaction_unequal_split['user_to_amount_map'],
                                                 'transaction_name': transaction_unequal_split['transaction_name']}
    params_for_balances = {'gpin': transaction_equal_split['gpin']}


@pytest.fixture(scope='function')
def get_expected_balances():
    return mock_balances.mock_balances_4_users_group


@pytest.mark.usefixtures("mock_transactions_and_balances", "setup", "post_request_params")
class TestGetUsersForGroup():

    @pytest.mark.order(1)
    @patch('utils.request_utils.get_response_for_post_request')
    @pytest.mark.parametrize("params_for_post_transaction",
                             ["params_for_post_transaction_equal_split", "params_for_post_transaction_unequal_split"])
    def test_when_transaction_between_4_users(self, mock_post_response, mock_transactions_and_balances, params_for_post_transaction):
        '''Test that call to post transactions is successful for 2 events between 4 users'''
        mock_post_response.return_value = mock_post_new_resource_request_response
        logging.info("Sending call to post transaction...")
        response_for_post_transaction = request_utils.get_response_for_post_request(url=url_post_transaction,
                                                                                    params=params_for_post_transaction)
        assert response_for_post_transaction.status_code == 201, "Post call to add transaction to group did not return 201"
        logging.info("Transaction successfully posted!")

    @pytest.mark.order(2)
    @patch('utils.request_utils.get_response_for_post_request')
    @pytest.mark.depends(on=['test_when_transaction_between_4_users'])
    def test_when_balance_calculated_between_4_users(self, mock_post_response, mock_transactions_and_balances):
        '''Test that call to calculate balance within a group is successful'''
        mock_post_response.return_value = mock_post_new_resource_request_response
        logging.info("Sending call to calculate balances for transactions within the group...")
        response_for_post_balances = request_utils.get_response_for_post_request(url=url_balance,
                                                                                    params=params_for_balances)
        assert response_for_post_balances.status_code == 201, "Post call to add balances to group did not return 201"
        logging.info("Balances successfully calculated and posted!")

    @pytest.mark.order(3)
    @patch('utils.request_utils.get_response_for_get_request')
    @pytest.mark.usefixtures("get_expected_balances")
    def test_correct_balances_were_calculated_between_4_users(self, mock_get_response, mock_transactions_and_balances, get_expected_balances):
        '''Test that the balances were correctly calculated among group users with minimum transactions needed to settle the balance'''
        mock_get_response.return_value = mock_balances_for_4_users_transactions
        logging.info("Sending call to fetch the calculated balances among group users...")
        response_for_get_balances = request_utils.get_response_for_get_request(url=url_balance, params=params_for_balances)
        logging.info("Asserting if call to fetch balances was successful...")
        assert response_for_get_balances.status_code == 200, "Get balances did not return a 200 status code."
        response_body = response_for_get_balances.data
        expected_response_body = get_expected_balances
        logging.info("Asserting if the balances were correctly calculated requiring minimum transactions among the users to settle...")
        for balance in response_body:
            assert balance.__dict__ in expected_response_body
        logging.info("Test passed!")