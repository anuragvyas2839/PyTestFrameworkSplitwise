import requests

from services.mock_auth_details import mock_http_basic_auth
from constants import url_endpoints

url_mapping = url_endpoints.url_mapping
base_url = url_endpoints.base_url
basic_header = {'Content-Type':'application/json'}

def get_endpoint_url(endpoint):
    '''Util function to create url for calling an endpoint'''
    return base_url + url_mapping[endpoint]

def get_response_for_get_request(url, header = basic_header, params = None):
    '''Util function perform a get request'''
    return requests.get(url=url, headers=header, params=params, auth=mock_http_basic_auth)

def get_response_for_post_request(url, header = basic_header, params = None, json=None):
    '''Util function perform a post request'''
    return requests.post(url=url, headers=header, params=params, json=json, auth=mock_http_basic_auth)