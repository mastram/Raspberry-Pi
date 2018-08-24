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

def send_data_to_vi(post_data) :
	url = vi.api_endpoint_url
	token = vi.oauth_token
	headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
	r = requests.post(url, data=json.dumps(post_data), headers=headers)
	return r.status_code
	

## Main Program ##

# GPS
gpsp = gps_poller.GpsPoller()
gpsp.start()
print(gpsp.get_polling_status())


# do 5 times to initialize
i = 0
while i<5:
    sensor_readings = sensor_data.get_sense_data()
    i = i+1

print("loop start")
i=0
start_time = time.time()
now = time.time()

try:

    while now < start_time + time_to_log:
	
	sensor_readings = sensor_data.get_sense_data()
	sensor_readings.append(comment)
	gps_data = gpsp.get_current_value()
	
	vehicle_data = {}
	vehicle_data["format"] = vi.tracking_device_id
	vehicle_data["TrackingDeviceID"] = vi.tracking_device_id
	vehicle_data["timestamp"] = 1000 * time.time()
	vehicle_data["readings"] = {}
	vehicle_data["readings"]["Speed"] = gps_data.fix.speed
	vehicle_data["readings"]["Acc_X"] = sensor_readings[10]
	vehicle_data["readings"]["Acc_Y"] = sensor_readings[11]
	vehicle_data["readings"]["Acc_Z"] = sensor_readings[12]
	vehicle_data["GPS"] = {}
	vehicle_data["GPS"]["coordinates"] = [gps_data.fix.longitude,gps_data.fix.latitude]
#	vehicle_data["GPS"]["SignalStrength"] = gps_data.satellites
#        vehicle_data["GPS"]["Heading"] = gps_data.fix.heading

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
