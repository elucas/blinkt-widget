import os

def add_new_data(received_data, ip_address):
    file = open('/home/pi/Desktop/blinkt_status/data/master_data', 'r+')
    text_to_append = ip_address + "," + received_data
    if file.read() == "":
        print("empty file")
        file.write(text_to_append)
        file.close()
        return
    else: #if there is something in the file (otherwise it will crash due to empty array...)
        file = open('/home/pi/Desktop/blinkt_status/data/master_data', 'r+')
        everyline=file.readlines()
        print ("This is what i read: "+ everyline[0])
        number_of_lines = how_many_lines()
        
        print("number of lines: " + str(number_of_lines))
        which_line = search_for_ip(number_of_lines, everyline, ip_address) #really should've added more comments

        everyline[(which_line -1)] = text_to_append +"\n"
        print(everyline[(which_line -1)])
        file = open('/home/pi/Desktop/blinkt_status/data/master_data', 'w')
        print (everyline[0])
        file.write("")
        file.writelines(everyline)
        file.close()    
    
    
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
    # the statuses of every user on the webpage or somewhere else...
    # perhaps the master pi could have more LEDs and display all statuses there...
    

def search_for_ip(lines, all_data, the_ip):
    a=0
    while a < lines:
        if all_data[a].split(',')[0] == the_ip:
            print("found it on line " + str(a+1))
            return (a+1)
        a+=1
        
    

  
def how_many_lines():
    i=0
    with open('/home/pi/Desktop/blinkt_status/data/master_data', 'r') as f:
        for i, l in enumerate(f):
            pass
    return (i + 1)
