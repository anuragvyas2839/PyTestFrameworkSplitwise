from entities.user import User
from entities.group import Group
from entities.transaction import Transaction
from entities.balances import Balances
from test_data import mock_users, mock_groups, mock_transactions, mock_balances


class MockRequestResponse:
    def __init__(self, data=None, status_code=200):
        self.data = data
        self.status_code = status_code


class MockUsersByGroup:
    def get_2_mock_users_for_group_1(self):
        data = [
            User(mock_users.user_1_details),
            User(mock_users.user_2_details)
        ]
        return MockRequestResponse(data)

    def get_1_mock_user_for_group_1(self):
        data = [
            User(mock_users.user_1_details)
        ]
        return MockRequestResponse(data)

    def get_no_group_found_for_group_2(self):
        return MockRequestResponse(data=[], status_code=404)


class MockUserDetails:
    def get_mock_user_details_group_1(self):
        data = User(mock_users.user_1_details)
        return MockRequestResponse(data)

    def get_mock_user_details_no_group(self):
        data = User(mock_users.user_1_details_no_group)
        return MockRequestResponse(data)


class MockGroup:
    def get_mock_group_with_2_users(self):
        data = Group(mock_groups.group_with_2_users)
        return MockRequestResponse(data)


class MockTransactions:
    def get_mock_transaction_with_4_users_equal_split(self):
        data = Transaction(mock_transactions.transaction_with_4_users_equal_split)
        return MockRequestResponse(data)

    def get_mock_transaction_with_4_users_unequal_split(self):
        data = Transaction(mock_transactions.transaction_with_4_users_unequal_split)
        return MockRequestResponse(data)


class MockBalances:
    def get_mock_balances_user4user3user2_owe_user1(self):
        mock_balance_user4_owes_user1 = mock_balances.mock_balances_4_users_group[0]
        gpin = mock_balance_user4_owes_user1['gpin']
        user_owed = mock_balance_user4_owes_user1['user_owed']
        user_owes = mock_balance_user4_owes_user1['user_owes']
        amount = mock_balance_user4_owes_user1['amount']
        object_balance_user4_owes_user1 = Balances(gpin, user_owed, user_owes, amount)
        mock_balance_user3_owes_user1 = mock_balances.mock_balances_4_users_group[1]
        gpin = mock_balance_user3_owes_user1['gpin']
        user_owed = mock_balance_user3_owes_user1['user_owed']
        user_owes = mock_balance_user3_owes_user1['user_owes']
        amount = mock_balance_user3_owes_user1['amount']
        object_balance_user3_owes_user1 = Balances(gpin, user_owed, user_owes, amount)
        mock_balance_user2_owes_user1 = mock_balances.mock_balances_4_users_group[1]
        gpin = mock_balance_user2_owes_user1['gpin']
        user_owed = mock_balance_user2_owes_user1['user_owed']
        user_owes = mock_balance_user2_owes_user1['user_owes']
        amount = mock_balance_user2_owes_user1['amount']
        object_balance_user2_owes_user1 = Balances(gpin, user_owed, user_owes, amount)
        data = [object_balance_user4_owes_user1, object_balance_user3_owes_user1, object_balance_user2_owes_user1]
        return MockRequestResponse(data)
