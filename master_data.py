import os

def add_new_data(received_data, ip_address):
    file = open('/home/pi/Desktop/blinkt_status/data/master_data', 'r+')
    #everyline=file.readlines()
    #print ("This is what i read: "+ everyline[0])
    file = open('/home/pi/Desktop/blinkt_status/data/master_data', 'w+')
    text_to_append = ip_address + "," + received_data
    file.write(text_to_append)
    file.close()
    print (text_to_append)

    # the idea is that the master_data files contains data about every pi.
    # it is structured as a csv file.
    # every "," comma is a new column and every line is a row.
    # 
    # a raspberry pi will send us the data. the data is then to be stored into
    # the file.
    # we must check which line the ip address is on.
    # then append the data and close the file.
    #
    #
    # the data file will be sent out to every pi so that it can display
    # the statuses of every user on the webpage.
    
    
