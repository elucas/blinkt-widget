import os
import json

#files to store information
CUR_STATUS_FILE = '/tmp/status'
STATUSES_FILE = '/tmp/statuses.json'
DEVICES_FILE= '/tmp/device'

def read_statuses():
    '''Read the list of statuses'''
    if os.path.isfile(STATUSES_FILE):
        with open(STATUSES_FILE, 'r') as cur_file:
            statuses = json.load(cur_file)
            return statuses
    else:
        return []

def set_statuses(statuses_list):
    '''Make a list of possible statuses on the current device'''
    with open(STATUSES_FILE,'w') as cur_file:
        json.dump(statuses_list, cur_file, indent=4)

#get and set status
def change_status(new_status):
    '''change the content of the file 'Blinkt_Status'''
    status = open(CUR_STATUS_FILE,'w')
    status.write(new_status)
    status.close() 


def get_status(default=None):
    """Get the current status value from the file"""
    status = default
    if os.path.isfile(CUR_STATUS_FILE):
        status_file = open(CUR_STATUS_FILE,'r')
        status = status_file.readline().strip()

    return status

def get_type():
    '''Read the device type'''
    if os.path.isfile(DEVICES_FILE):
        with open(DEVICES_FILE, 'r') as cur_file:
            device_type = cur_file.readline().strip()
            return device_type
    else:
        return ''

def set_type(dev_type):
    '''Store the device type, given by lightswitch.py or demo.py'''
    with open(DEVICES_FILE, 'w') as cur_file:
        cur_file.write(dev_type)

