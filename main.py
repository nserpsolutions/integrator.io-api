import library.integrator_io_api_lib as iial

io_instance = input('integrator.io instance: ')
if io_instance == 'EU':
    base_uri = 'api.eu.integrator.io'
else:
    base_uri = 'api.integrator.io'

flow_id = input('Enter Flow ID: ')
component_id = input('Enter Export/Import ID: ')
api_token = input('Enter API Token: ')

request_headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}

retry_data_list = iial.get_error_data(base_uri, flow_id, component_id, request_headers)
iial.create_files(retry_data_list)