import logging
import pytest
from unittest.mock import patch
from datetime import date

from services.create_mock_entities import MockUsersByGroup
from utils import request_utils


@pytest.fixture(scope='class')
def setup()->None:
    '''Setup urls needed in the test class'''
    global url
    url = request_utils.get_endpoint_url('get_user_details_in_group')


@pytest.fixture(scope='class')
def mock_users()->None:
    '''Get mock entities needed in the test class'''
    global two_mock_users_for_group_1, no_group_found_for_group_2, single_mock_user_for_group_1
    mock_users_by_group = MockUsersByGroup()
    two_mock_users_for_group_1 = mock_users_by_group.get_2_mock_users_for_group_1()
    single_mock_user_for_group_1 = mock_users_by_group.get_1_mock_user_for_group_1()
    no_group_found_for_group_2 = mock_users_by_group.get_no_group_found_for_group_2()

@patch('utils.request_utils.get_response_for_get_request')
@pytest.mark.usefixtures("mock_users", "setup")
class TestGetUsersForGroup():

    @pytest.mark.order(1)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_when_two_users_in_group(self, mock_users_by_group, mock_users, setup):
        '''Test if correct details of users are returned for a group with 2 users'''
        mock_users_by_group.return_value = two_mock_users_for_group_1
        logging.info("Sending call to get user details for a group with 2 users...")
        response = request_utils.get_response_for_get_request(url=url, params={'group_id':1})
        response_body = response.data
        logging.info("Response received, asserting on details now...")
        assert response.status_code == 200
        assert len(response_body) == 2
        assert response_body[0].username == 'user1@gmail.com', "Username is not as expected for user1 in group 1"
        assert response_body[1].username == 'user2@gmail.com', "Username is not as expected for user2 in group 1"
        assert response_body[0].first_name == 'user1_fn', "First name is not as expected for user1 in group 1"
        assert response_body[1].first_name == 'user2_fn', "First name is not as expected for user2 in group 1"
        assert response_body[0].last_name == 'user1_ln', "Last name is not as expected for user1 in group 1"
        assert response_body[1].last_name == 'user2_ln', "Last name is not as expected for user2 in group 1"
        assert response_body[0].dob == date(1993, 11, 28), "Date of birth is not as expected for user1 in group 1"
        assert response_body[1].dob == date(1993, 11, 17), "Date of birth is not as expected for user2 in group 1"
        logging.info("Test passed!")

    @pytest.mark.order(2)
    @pytest.mark.regression
    def test_when_single_user_in_group(self, mock_users_by_group, mock_users, setup):
        '''Test if correct details of users are returned for a group with only 1 user'''
        mock_users_by_group.return_value = single_mock_user_for_group_1
        logging.info("Sending call to get user details for a group with single user...")
        response = request_utils.get_response_for_get_request(url=url, params={'group_id': 1})
        response_body = response.data
        logging.info("Response received, asserting on details now...")
        assert response.status_code == 200
        assert len(response_body) == 1
        assert response_body[0].username == 'user1@gmail.com'
        logging.info("Test passed!")

    @pytest.mark.order(3)
    @pytest.mark.regression
    def test_when_group_name_non_existent(self, mock_users_by_group, mock_users, setup):
        '''Test if appropriate http response is returned if api to get user details called for non existing group name'''
        mock_users_by_group.return_value = no_group_found_for_group_2
        logging.info("Sending call to get user details from a non existing group name...")
        response = request_utils.get_response_for_get_request(url=url, params={'group_id':2})
        response_body = response.data
        logging.info("Asserting response status code...")
        assert response.status_code == 404
        assert len(response_body) == 0
        logging.info("Test passed!")