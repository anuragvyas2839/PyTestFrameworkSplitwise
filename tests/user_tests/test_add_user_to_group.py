import pytest
import logging
from unittest.mock import patch

from services.create_mock_entities import MockUserDetails, MockRequestResponse, MockGroup
from utils import request_utils
from test_data import mock_users

@pytest.fixture(autouse=True, scope='class')
def setup() -> None:
    '''Setup urls needed in the test class'''
    global url_add_user_to_group, url_get_user, url_get_users_in_group
    url_add_user_to_group = request_utils.get_endpoint_url('add_user_to_group')
    url_get_user = request_utils.get_endpoint_url('get_user_by_id')
    url_get_users_in_group = request_utils.get_endpoint_url('get_users_in_group')


@pytest.fixture(autouse=True, scope='class')
def mock_users_and_groups() -> None:
    '''Get mock entities needed in the test class'''
    global mock_post_request_response, mock_user_details_no_group, mock_user_details_group_1, mock_group_with_2_users, mock_post_request_response_existing_user
    mock_post_request_response = MockRequestResponse()
    mock_post_request_response_existing_user = MockRequestResponse(data={'message': 'User is already part of group.'})
    mock_user_details = MockUserDetails()
    mock_group = MockGroup()
    mock_user_details_no_group = mock_user_details.get_mock_user_details_no_group()
    mock_user_details_group_1 = mock_user_details.get_mock_user_details_group_1()
    mock_group_with_2_users = mock_group.get_mock_group_with_2_users()

@pytest.fixture(autouse=True, scope='class')
def post_request_params() -> None:
    '''Create params needed for api calls in the test class'''
    global upin, params_for_post
    upin = mock_users.user_1_details_no_group['upin']
    params_for_post = {'upin': upin, 'group_id': 1}


@pytest.mark.usefixtures("mock_users_and_groups", "setup", "post_request_params")
class TestGetUsersForGroup():

    @pytest.mark.order(1)
    @pytest.mark.smoke
    @pytest.mark.regression
    @patch('utils.request_utils.get_response_for_get_request')
    @patch('utils.request_utils.get_response_for_post_request')
    def test_when_new_user_added_to_group(self, mock_post_response, mock_user_details):
        '''
            1. Test that user is not already part of the group
            2. Add user to the group
            3. Assert that user is now added to the group
        '''
        mock_post_response.return_value = mock_post_request_response
        mock_user_details.side_effect = [mock_user_details_no_group, mock_user_details_group_1, mock_group_with_2_users]
        logging.info("Checking if user already exists in group...")
        response_for_get_user = request_utils.get_response_for_get_request(url=url_get_user, params={'upin': upin})
        response_body = response_for_get_user.data
        # assert that test user is not already part of the group
        assert 1 not in response_body.groups, "Test user is already part of the group"
        logging.info("Sending request to add user to the group...")
        response_for_post_user = request_utils.get_response_for_post_request(url=url_add_user_to_group,
                                                                             params=params_for_post)
        # assert that post call was successful and returned a 200
        assert response_for_post_user.status_code == 200, "Post call to add user to group did not return 200"
        logging.info("Checking if group id got added in the user's groups...")
        response_for_get_user = request_utils.get_response_for_get_request(url=url_get_user)
        response_body = response_for_get_user.data
        # assert that group is added in test user details
        assert 1 in response_body.groups, "Group not getting added to user details"
        logging.info("Checking that user also got added to the group's users...")
        response_for_get_group_users = request_utils.get_response_for_get_request(url=url_get_users_in_group)
        response_body = response_for_get_group_users.data
        # assert that test user is also added in the group
        assert upin in response_body.users, "User not getting added to the group"
        logging.info("Test passed!")

    @pytest.mark.order(2)
    @pytest.mark.depends(on=['test_when_new_user_added_to_group'])
    @pytest.mark.regression
    @patch('utils.request_utils.get_response_for_post_request')
    def test_when_existing_user_added_to_group(self, mock_post_response):
        '''Test when a user already existing in a group is requested to be added to the group'''
        mock_post_response.return_value = mock_post_request_response_existing_user
        logging.info("Sending request to add user to a group it is already part of.")
        response_for_post_user = request_utils.get_response_for_post_request(url=url_add_user_to_group,
                                                                             params=params_for_post)
        assert response_for_post_user.status_code == 200 # not expecting a 409 as it is for case of conflict in new and existing resource
        assert response_for_post_user.data['message'] == 'User is already part of group.'
        logging.info("Test passed!")