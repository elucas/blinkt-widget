import requests
import avahi

from flask import Flask, request, render_template, make_response, current_app, json, Response, jsonify, redirect, url_for

app = Flask(__name__)

def get_device_list():
	'''Returns a list of ips of devices'''
	device_list = []
	avahi.run()
	blinkt_devices = avahi.read()
	print(blinkt_devices)
	for item in blinkt_devices:
		device_list.append(item)
	print(device_list)
	return device_list
	
def get_device_statuses():
	statuses = []
	device_list = get_device_list()
	for device in device_list:
		#This line would make http://localhost:5000 into http://localhost:5000/api
		device = device.strip()
		print('http://' + device + '/api')
		try:
			response = requests.get('http://' + device + '/api', timeout=1)
			print(response)
			#builds a dict list of statuses and the type of device
			statuses.append(response.json())
		except:
			statuses.append({'missing' : device})
		
	return statuses

@app.route('/', methods=['GET'])
def main():
	return render_template('dashboard.html', statuses=get_device_statuses())
	
@app.route('/',methods=['POST'])
def change():
	the_new_status = request.form['new_status']
	endpoint = request.form['endpoint']
	#changes the status of the relevant device by calling api.refresh()
	requests.post(endpoint, data = { 'new_status': the_new_status })
	#status.change_status(the_new_status)
	return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001, threaded=True)
