#!/usr/bin/env python
"""Query avahi and log all the machines advertising a blinkt service
"""
import subprocess

SERVICE = '_blinkt._tcp'
BLINKT_DEVICES = '/tmp/blinkt_devices'

def browse():
    """Call the avahi-browse program installed using 'apt-get install avahi-utils'

    Example output (partial):

= enp3s0 IPv4 status1                                       _blinkt._tcp         local
   hostname = [status1.local]
   address = [192.168.55.35]
   port = [5000]
   txt = ["good=innit"]

    """
    # -t : terminate after running
    stdout = subprocess.check_output(['avahi-browse', '-t', '--resolve', '--all'])

    matches = []
    in_match = False
    for line in stdout.split("\n"):
        # Look for lines starting with "="
        if line[0:1] == "=":
            if SERVICE in line and "IPv4" in line:
                in_match = True
                continue
            else:
                in_match = False
                continue

        if in_match:
            # e.g. "    address = [192.168.55.111]"
            if "address" in line:
                # Pull out the address
                address = line[line.index('[')+1:line.index(']')]
            if "port" in line:
                # Pull out the port and add it to the list
                hostname = address + ':' + line[line.index('[')+1:line.index(']')]
                matches.append(hostname)
    return matches

def write(devices):
    file = open(BLINKT_DEVICES, 'w')
    for device in devices:
        file.write(device + '\n')
    file.close()
    print "Written"

def read():
    with open(BLINKT_DEVICES, 'r') as file:
        lines = file.readlines()
        blinkt_devices_list = []
        for line in lines:
            line = line.strip()
            blinkt_devices_list.append(line)
        return blinkt_devices_list

def run():
    if __name__ == "__main__":
        matches = browse()

        print "Matches..."
        for match in matches:
            print match
            
        write(matches)
run()
