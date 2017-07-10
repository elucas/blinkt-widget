import os

#this file holds the values for different statuses

                              ###   Contents of dictionaries inside STATUSES   ###
    #title = words at top of page
    #label = words on button
    #name = name of dictionary
    #lights = which type of lights are shown (solid_colour, flashing, etc.) - MUST be a valid function in display program
    #monocolour = is the colour chosen in the dictionary or set inside the function? Is only one colour used? 'yes'/'no'
    #red,green,blue = if colour decided in dictionary, what colour is it? - NOT required if monocolour = False

#all dictionary content can be changed and new dictionaries can be made, but the above attributes are REQUIRED
#when changed no other code needs to be changed
STATUSES = {
    'available' : {'name': 'available', 'title': "User is Available", 'label': "Available", 'lights': 'solid_colour', 'monocolour': 'yes', 'red': 0, 'green': 255, 'blue': 0},
    'busy' : {'name': 'busy', 'title': "User is Busy", 'label': "Busy", 'lights': 'solid_colour', 'monocolour': 'yes', 'red': 255, 'green': 0, 'blue': 0},
    'disturbable' : {'name': 'disturbable', 'title': "User is Slightly busy", 'label': "Busy-ish", 'lights': 'solid_colour', 'monocolour': 'yes', 'red': 94, 'green': 18, 'blue': 0},
    'finding' : {'name': 'finding', 'title':"User is Finding Blinkt", 'label': "Find", 'lights': 'animation', 'monocolour': 'yes', 'red': 0, 'green': 0, 'blue': 255},
    'party' : {'name': 'party', 'title':"User is PARTYING", 'label': "!PARTY!", 'lights': 'party', 'monocolour': 'no', 'length': 10},
    }

status_file = '/tmp/Blinkt_Status' 

def change_status(new_status):
    #change the content of the file 'Status'
    status = open(status_file,'w')
    status.write(new_status)

def get_status():
    # check that the file exists yet
    if os.path.exists(status_file):
        file = open(status_file,'r')
        status = file.readline()
        #checks that the current status is in STATUSES
        if status in STATUSES:
            return STATUSES[status]
        else:
            return False
    else:
        #if file doesn't exist, make it
        change_status('available')
        os.chmod(status_file, 0o666)

