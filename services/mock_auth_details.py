# real credentials should be picked from a secure place like vault, not to be stored in a file
from requests.auth import HTTPBasicAuth

mock_credentials = {
    'user': 'mock_auth_user',
    'password': 'mock_auth_password#123',
}

mock_http_basic_auth = HTTPBasicAuth(mock_credentials['user'], mock_credentials['password'])