params = {
    'param1': 'value1',
    'param2': 'value2'
}

headers = {
    'Authorization': 'Bearer your_token',
    'Content-Type': 'application/json'
}
import requests
from requests.exceptions import HTTPError, Timeout

try:
    response = requests.get('http://127.0.0.1:5000', params=params, headers=headers)
    response.raise_for_status()  # Raise an exception for 4xx/5xx responses
    data = response.json()       # Parse the JSON data
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Timeout as timeout_err:
    print(f"Request timed out: {timeout_err}")
except Exception as err:
    print(f"An error occurred: {err}")
