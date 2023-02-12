import library.integrator_io_api_lib as iial
from library.IoApi import IoApi

io_instance = input('integrator.io instance: ')
if io_instance == 'EU':
    base_uri = 'api.eu.integrator.io'
else:
    base_uri = 'api.integrator.io'

flow_id = input('Enter Flow ID: ')
component_id = input('Enter Export/Import ID: ')
api_token = input('Enter API Token: ')

io_connection = IoApi(base_uri, api_token)

retry_data_list = io_connection.get_error_data(flow_id, component_id)
iial.create_files(retry_data_list)