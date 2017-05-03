import requests
import time

base_url = 'http://10.0.0.62/api/'
apikey = {'apikey': 'E5168A6891C24B54919023C4D162B1DA'}


def get_connection_status():
    r = requests.get(base_url + 'connection', params=apikey)
    return r.json()["current"]["state"]


def connect_to_printer():
    command_data = {'command': 'connect', 'baudrate': 115200, 'printerProfile': 'prusa_i3_mk2'}
    r = requests.post(base_url + 'connection', json=command_data, params=apikey)
    return r


def upload_stl(filename):
    file = {'file': (filename, open(filename, 'rb'), 'application/octet-stream')}
    r = requests.post(base_url + 'files/local', files=file, params=apikey)
    return r


def slice_and_select(filename):
    command_parameters = {'command': 'slice',
                          'position': {'x': 125, 'y': 105},
                          'printerProfile': 'prusa_i3_mk2',
                          'profile': 'original_prusa_i3_mk2_0_15_pla_normal',
                          'select': True}
    r = requests.post(base_url + 'files/local/' + filename, json=command_parameters, params=apikey)
    return r

def get_print_job_info():
    return requests.get(base_url + 'job', params=apikey).json()

def start_print_job():
    start_command = {'command': 'start'}
    return requests.post(base_url + 'job', json=start_command, params=apikey)


def print_stl_file(filename):
    # Check current printer status and try to connect if necessary
    current_status = get_connection_status()
    print('Current printer connection status: ' + current_status)
    if current_status == 'Closed':
        print('Connecting to printer:')
        connect_to_printer()
        current_status = get_connection_status()
        print('\t' + current_status)
        while current_status != 'Operational':
            time.sleep(2)
            current_status = get_connection_status()
            print('\t' + current_status)

    # Upload stl file to OctoPrint
    file_upload_response = upload_stl(filename)
    if file_upload_response.json()['done']:
        print('File "' + filename + '" uploaded successfully')
    else:
        print('Failed to upload ' + filename)
        exit()

    # Slice stl file to gcode
    slice_and_select(filename)
    print('Preparing file for printing; please wait...')

    # Retrieve print info once slicing is complete
    print_job_info = get_print_job_info()
    while(print_job_info['job']['estimatedPrintTime'] == None):
        time.sleep(10)
        print_job_info = get_print_job_info()
    print('Estimated print time: ' + str(print_job_info['job']['estimatedPrintTime'] / 60) + ' minutes')

    # Start print job
    start_print_job()
    print('Printing started!')



#print_stl_file('brailleHelloWorld_thin.stl')
