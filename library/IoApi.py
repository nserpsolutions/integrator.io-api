import requests

class IoApi:
    def __init__(self, base_uri, api_token):
        self.base_uri = base_uri
        self.version = 'v1'
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Accept': 'application/json'
        }
    
    def __str__(self):
        return f'{self.base_uri},{self.version}'
    
    def get_error_data(self, flow_id, component_id):
        errors_response = requests.get(f'https://{self.base_uri}/{self.version}/flows/{flow_id}/{component_id}/errors', headers = self.headers)
        error_details = errors_response.json()
        retry_data_list = []
        
        for error_info in error_details['errors']:
            retry_data_key = error_info['retryDataKey']
            retry_data_response = requests.get(f'https://{self.base_uri}/{self.version}/flows/{flow_id}/{component_id}/{retry_data_key}/data', headers = self.headers)
            retry_data = retry_data_response.json()
            retry_data_list.append(retry_data['data'])
        
        return retry_data_list
