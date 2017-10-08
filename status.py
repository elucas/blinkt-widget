import os
import requests
import ConfigParser
import json
import subprocess


# CONFIG OPTIONS
# name of device?

#list of statuses
#to add a status
    #add appropiate response to status in blinkt_display_status
    #add on webpage.py the approproate image and defining color of status
#STATUSES = ['available', 'busy', 'disturbable', 'finding', 'party', 'alert', 'offline']

#list of Pi's and their respective IPs on the network
MASTER_IP = "192.168.55.116"

#files to store information
STATUS_FILE = '/tmp/blinkt_status'

CONFIG_FILE = 'blinkt-widget.conf'
CONFIG_DEFAULTS = {
    'status': {
        'name': 'blinkt-widget'
    },
    'web': {
        'port': 5000,
        'password': None
    }
}

name_file = '/home/pi/Desktop/blinkt_status/data/blinkt_name'
ip_file = '/home/pi/Desktop/blinkt_status/data/blinkt_ips'
PROFILE_FILE = '/home/pi/Desktop/blinkt_status/data/blinkt_profiles'
hash_file = '/home/pi/Desktop/blinkt_status/data/blinkt_hash'
salt_file = '/home/pi/Desktop/blinkt_status/data/blinkt_salt'
#ip_file is redundant at the moment

#this is to set and get the Pi's own IP - redundant at the moment
def get_self_ip():
    #essentially "hostname -I" in terminal
    my_ip = subprocess.check_output(["hostname", "-I"])
    #subprocess returns variable in bytes --> let's convert it into a string
    string = my_ip.decode("utf-8")
    #now we have the ip without the utf-6 encoding! 
    print ("This pi's ip:" + string)
    #(you can use "print (type(variable))" to check a variable's type)
    return string
    
#where is this function used?...    
def set_ip(new_ip):
    file = open(ip_file, 'w')
    file.write(new_ip)

#get and set name
def get_name():
    if os.path.exists(name_file):
            file = open(name_file, 'r')
            name = file.readline()
            print (name)
            return name
    else:
        return "no-name"
    
def set_name(new_name):
    print ("Setting new name!")
    file = open(name_file, 'w')
    file.write(new_name)
    file.close()
    url = "http://" + MASTER_IP + ":5000/register"
    info = get_status() + ',' + new_name
    r = requests.post(url, json=info, timeout=2)
    print ("sent new name!")
    return "Hey"


#get and set status
def change_status(new_status):
    #change the content of the file 'Blinkt_Status'
    status = open(STATUS_FILE,'w')
    status.write(new_status)
    status.close()
    url = "http://" + MASTER_IP + ":5000/register"
    info = new_status + ','  + get_name()
    requests.post(url, json=info, timeout=5)    
    print ("sent new status!")


def get_status():
    """Get the current status value from the file"""
    status = None
    if os.path.isfile(STATUS_FILE):
        status_file = open(STATUS_FILE,'r')
        status = status_file.readline().strip()

    # TODO: Why not remove the fallback clause and let actions.py decide the default action?
    if not status:
        status = "available"
    return status


def load_config(config_file=CONFIG_FILE):
    """Load the config file, if present. Otherwise return defaults."""
    if os.path.isfile(config_file):
        config = ConfigParser.SafeConfigParser(CONFIG_DEFAULTS)
        config.read(config_file)


def get_hash():
    file = open(hash_file, 'r')
    the_hash = file.readline()
    return the_hash

def get_salt():
    file = open(salt_file, 'r')
    the_salt = file.readline()
    return the_salt

def set_hash(new_hash):
    file = open(hash_file, 'w')
    file.write(new_hash)

def set_salt(new_salt):
    file = open(salt_file, 'w')
    file.write(new_salt)
    


