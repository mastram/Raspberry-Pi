############################
##   Vehicle Data Logging  ##
############################
from modules.sense_hat  import sensor_data
from modules.gps_poller import gps_poller
from modules.config import vi
import time
import argparse
import json
import requests

### Logging Settings ###


### Argument Handling ###
parser = argparse.ArgumentParser()
parser.add_argument("-ttl",help="Time to log",type=int,default=1)
parser.add_argument("-comment",help="Comment",default="Test Logging")

args = parser.parse_args()

time_to_log = args.ttl
comment = args.comment

def get_fuel_estimation(speed) :
	if speed <= 3 : return 1
	elif  speed > 3 and speed <= 10 : return speed / 10
	elif  speed > 10 and speed <= 20 : return speed / 11
	elif  speed > 20 and speed <= 30 : return speed / 12
	elif  speed > 30 and speed <= 40 : return speed / 13
	elif  speed > 40 and speed <= 50 : return speed / 14
	elif  speed > 50 and speed <= 60 : return speed / 15
	elif  speed > 60 : return speed / 16
	else : return 1

def send_data_to_vi(post_data) :

	try:
		url = vi.api_endpoint_url
		token = vi.oauth_token
		headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
		r = requests.post(url, data=json.dumps(post_data), headers=headers)
		return r.status_code
	except requests.exceptions.RequestException as e:
#		Ignore if we are unable to post to web service
		return -1;
	

## Main Program ##

# GPS
gpsp = gps_poller.GpsPoller()
gpsp.start()
print(gpsp.get_polling_status())


# do 5 times to initialize
i = 0
while i<5:
    sensor_readings = sensor_data.get_sense_data()
    gps_data = gpsp.get_current_value()
    i = i+1

print("loop start")
i=0
start_time = time.time()
now = time.time()

try:

	sensor_readings = sensor_data.get_sense_data()
	sensor_readings.append(comment)
	gps_data = gpsp.get_current_value()
	
	vehicle_data = {}
	vehicle_data["format"] = vi.tracking_device_id
	vehicle_data["TrackingDeviceID"] = vi.tracking_device_id
	vehicle_data["timestamp"] = 1000 * time.time()
	vehicle_data["readings"] = {}
	vehicle_data["readings"]["Speed"] = gps_data.fix.speed * 3.6	#mps to kmph
	vehicle_data["readings"]["OBDII_1_5E"] = get_fuel_estimation(vehicle_data.readings.speed)	#mps to kmph
	vehicle_data["readings"]["Acc_X"] = sensor_readings[10]
	vehicle_data["readings"]["Acc_Y"] = sensor_readings[11]
	vehicle_data["readings"]["Acc_Z"] = sensor_readings[12]
	vehicle_data["GPS"] = {}
	vehicle_data["GPS"]["coordinates"] = [gps_data.fix.longitude,gps_data.fix.latitude]
#	vehicle_data["GPS"]["SignalStrength"] = gps_data.satellites
#   vehicle_data["GPS"]["Heading"] = gps_data.fix.heading

#	print(json.dumps(vehicle_data))

	status_code = send_data_to_vi(vehicle_data)
#	print('Post Response', status_code)
	print('Data Posted at ', time.time())

	time.sleep(2)

except(KeyboardInterrupt, SystemExit):
#   Stop Polling now
    gpsp.stop_polling()
    print(gpsp.get_polling_status())
    gpsp.join()


print("program complete")
