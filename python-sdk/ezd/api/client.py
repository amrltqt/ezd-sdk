import json
import os
import requests

from ezd.api.exception import APIException

DEFAULT_API_URL = 'https://api.ezd.amrltqt.com'


class EZDClient:
    """
    Client class for interacting with the My API.
    """

    def __init__(self, base_url, api_key=None):
        """
        Initialize the client.

        Args:
            base_url (str): The base URL of the My API.
            api_key (str, optional): An API key for authentication, if required.
        """
        self.base_url = base_url
        self.api_key = api_key

    @classmethod
    def from_env(cls):
        """
        Initialize the client from environment variables.

        Returns:
            EZDClient: An instance of the client.
        """
        base_url = os.environ.get('EZD_API_URL', DEFAULT_API_URL)
        api_key = os.environ.get('EZD_API_KEY')
        return cls(base_url, api_key)

    def _get_headers(self):
        """
        Helper method to generate headers for API requests, including authentication headers if applicable.

        Returns:
            dict: A dictionary of headers.
        """
        headers = {
            'Content-Type': 'application/json',
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def _make_request(self, method, path, data=None, params=None):
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.).
            path (str): API endpoint path.
            data (dict, optional): JSON data to send with the request.
            params (dict, optional): Query parameters.

        Returns:
            requests.Response: The HTTP response object.
        """
        url = f"{self.base_url}/{path}"
        headers = self._get_headers()

        try:
            response = requests.request(method, url, json=data, params=params, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            # Handle exceptions and raise custom exceptions if needed
            raise APIException(f"Request to {url} failed: {e}")

    def list_dashboards(self):
        """
        List dashboards from your organisation.
        Only 1000 first results (no one should have that much dashboards!!) are returned.

        Returns:
            list: A list of resource objects.
        """
        response = self._make_request('GET', 'dashboards', params={"limit": 1000})
        return response.json()["results"]


    def get_dashboard(self, dashboard_id):
        """
        Get a dashboard from your organisation.

        Args:
            dashboard_id (str): The ID of the dashboard to retrieve.

        Returns:
            dict: A resource object.
        """
        response = self._make_request('GET', f'dashboards/{dashboard_id}')
        return response.json()
    

    def distribute_dashboard(self, dashboard_id, variables=None, targets=None):
        """
        Distribute a dashboard to a list of targets.

        Args:
            dashboard_id (str): The ID of the dashboard to distribute.
            variables (dict, optional): A dictionary of variables to replace in the dashboard.
            targets (list, optional): A list of targets to distribute the dashboard to.

        Returns:
            dict: A resource object.
        """

        
        data = {}
        if variables:
            data["variables"] = variables
        
        if targets:
            data["targets"] = targets
            
        response = self._make_request('POST', f'dashboards/{dashboard_id}/distribute', data=data)
        return response.json()