import os
import requests
import status

def poll_server():
    url = "http://" + status.MASTER_IP + ":5000/getStatuses"
    result = requests.get(url, params={'PROFILE' : ["value"]})
    file = open(status.PROFILE_FILE, 'w+')
    #print result
    file.write(result['PROFILE'])
    file.close()

poll_server()
