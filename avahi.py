#!/usr/bin/env python
"""Query avahi and log all the machines advertising a blinkt service
"""
import subprocess

SERVICE = '_blinkt._tcp'


def browse():
    """Call the avahi-browse program installed using 'apt-get install avahi-utils'"""
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
                # Pull out the address and add it to list
                matches.append(
                    line[line.index('[')+1:line.index(']')]
                )
    return matches


if __name__ == "__main__":
    matches = browse()
    for match in matches:
        print match

