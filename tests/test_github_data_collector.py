from GitHub_Cata_Collector.github_data_collector import fetch_github_data
import requests
from unittest.mock import patch

def test_fetch_github_data_successful():
    # Mocking the requests library to return a successful response
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'name': 'test_repo'}
        
        result = fetch_github_data('test_user', 'test_repo')
        
        assert result == {'name': 'test_repo'}

def test_fetch_github_data_failure():
    # Mocking the requests library to return a failed response
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value.status_code = 404
        
        result = fetch_github_data('nonexistent_user', 'nonexistent_repo')
        
        assert result is None
 