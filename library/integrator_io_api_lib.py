import requests
import json
import pandas as pd
import pathlib

def create_files(retry_data_list):
    dl_folder = pathlib.Path(pathlib.Path.home(), 'Downloads')
    if not dl_folder.is_dir():
        dl_folder = pathlib.Path(pathlib.Path.home())
    
    with open(pathlib.Path(dl_folder, 'error_data.json'), 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(retry_data_list, indent=4, ensure_ascii=False))
    
    csv_dataframe = pd.json_normalize(expand_nested_json_list(retry_data_list))
    csv_dataframe.to_csv(pathlib.Path(dl_folder, 'error_data.csv'), encoding='utf-8', index=False)

def get_error_data(base_uri, flow_id, component_id, request_headers):
    errors_response = requests.get(f'https://{base_uri}/v1/flows/{flow_id}/{component_id}/errors', headers = request_headers)
    error_details = errors_response.json()
    retry_data_list = []
    
    for error_info in error_details['errors']:
        retry_data_key = error_info['retryDataKey']
        retry_data_response = requests.get(f'https://{base_uri}/v1/flows/{flow_id}/{component_id}/{retry_data_key}/data', headers = request_headers)
        retry_data = retry_data_response.json()
        retry_data_list.append(retry_data['data'])
    
    return retry_data_list

def expand_nested_json_list(input_list):
    process_again = True
    while process_again:
        process_again = False
        new_list = []
        
        for data in input_list:
            array_found = False
            list_keys = data.keys()
            
            for list_key in list_keys:
                if type(data[list_key]) is list:
                    process_again = True
                    array_found = True
                    for sub_data in data[list_key]:
                        new_data = data.copy()
                        new_data[list_key] = sub_data
                        new_list.append(new_data)
                    break
            
            if not array_found:
                new_data = data.copy()
                new_list.append(new_data)
        
        input_list = new_list.copy()
    
    return input_list
