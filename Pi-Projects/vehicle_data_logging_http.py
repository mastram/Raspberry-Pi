############################
##   Vehicle Data Logging  ##
############################
from modules.sense_hat  import sensor_data
from modules.gps_poller import gps_poller
from modules.config import vi
from modules.database  import mysql_db

import time
import argparse
import json
import requests

### Logging Settings ###


### Argument Handling ###
parser = argparse.ArgumentParser()
parser.add_argument("-output",help="Print Results or not",type=int,default=0)
parser.add_argument("-comment",help="Comment",default="Test Logging")

args = parser.parse_args()

to_print = False
if args.output == 1 : to_print = True

comment = args.comment
fuel_level = 0;

def print_text(text) :
	if to_print : print text

def get_fuel_estimation(speed) :
	if speed <= 5 : return 1
	elif  speed > 5 and speed <= 10 : return speed / 8
	elif  speed > 10 and speed <= 20 : return speed / 9
	elif  speed > 20 and speed <= 30 : return speed / 10
	elif  speed > 30 and speed <= 40 : return speed / 11
	elif  speed > 40 and speed <= 50 : return speed / 12
	elif  speed > 50 and speed <= 60 : return speed / 14
	elif  speed > 60 : return speed / 16
	else : return 1

def send_data_to_vi(post_data) :
    
    try:
        url = vi.api_endpoint_url
        token = vi.oauth_token
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        r = requests.post(url, data=json.dumps(post_data), headers=headers)
        return r.status_code
    
    except:
        return -1
	
def get_current_fuel_value() :
	mysql_cur = mysql_db.get_cursor()
	query = "SELECT FuelLevel FROM `vehicle_data` WHERE VehicleID = 'KA53MB6956'"
	mysql_cur.execute(query)
	row = mysql_cur.fetchone()
	return row[0]

def update_fuel_value(fuel_value) :
	value_set = []
	value_set.append(fuel_value)
	mysql_cur = mysql_db.get_cursor()
	query = "UPDATE `vehicle_data` SET `FuelLevel` = %s WHERE VehicleID = 'KA53MB6956'"
	mysql_cur.execute(query, value_set)
	mysql_db.commit_data()


def send_ignition_status_to_vi(igni_status) :
	gps_data = gpsp.get_current_value()
	vehicle_data = {}
	vehicle_data["format"] = vi.tracking_device_id
	vehicle_data["TrackingDeviceID"] = vi.tracking_device_id
	vehicle_data["timestamp"] = 1000 * time.time()
	vehicle_data["readings"] = {}
	vehicle_data["readings"]["IgnitionStatus"] = igni_status
	vehicle_data["GPS"] = {}
	vehicle_data["GPS"]["coordinates"] = [gps_data.fix.longitude,gps_data.fix.latitude]
	status_code = send_data_to_vi(vehicle_data)
	print_text("Ignition Status Posted at " + str(time.time()) + " Status Code:" + str(status_code))

def send_fuel_data_to_vi() :
	gps_data = gpsp.get_current_value()
	vehicle_data = {}
	vehicle_data["format"] = vi.tracking_device_id
	vehicle_data["TrackingDeviceID"] = vi.tracking_device_id
	vehicle_data["timestamp"] = 1000 * time.time()
	vehicle_data["readings"] = {}
	vehicle_data["readings"]["FuelLevel"] = fuel_level
	vehicle_data["GPS"] = {}
	vehicle_data["GPS"]["coordinates"] = [gps_data.fix.longitude,gps_data.fix.latitude]
	status_code = send_data_to_vi(vehicle_data)
	print_text("Fuel Data Posted at " + str(time.time()) + " Status Code:" + str(status_code))

## Main Program ##

# Open MySQL Connection
mysql_db.open_connection()

# GPS
gpsp = gps_poller.GpsPoller()
gpsp.start()
print_text(gpsp.get_polling_status())


# do 5 times to initialize
i = 0
while i<5:
    sensor_readings = sensor_data.get_sense_data()
    gpsp.get_current_value()
    i = i+1

print_text("Loop Start")
#print("loop start")
i=0
prev_time = time.time()

try:

#	Send Ignition Status - ON
	send_ignition_status_to_vi("On")
    
#	Get the current fuel level
	fuel_level = get_current_fuel_value()

#	Send Fuel Level at the start
	send_fuel_data_to_vi()

    	while True:

		i = i + 1

	    	if i % 15 == 0: update_fuel_value(fuel_level)

	        sensor_readings = sensor_data.get_sense_data()
        	sensor_readings.append(comment)
	        gps_data = gpsp.get_current_value()

        	now = time.time()

	        vehicle_data = {}
	        vehicle_data["format"] = vi.tracking_device_id
	        vehicle_data["TrackingDeviceID"] = vi.tracking_device_id
	        vehicle_data["timestamp"] = 1000 * now
        	vehicle_data["readings"] = {}
	        vehicle_data["readings"]["Speed"] = gps_data.fix.speed * 3.6	#mps to kmph
        	vehicle_data["readings"]["Acc_X"] = sensor_readings[10]
	        vehicle_data["readings"]["Acc_Y"] = sensor_readings[11]
        	vehicle_data["readings"]["Acc_Z"] = sensor_readings[12]
        
	        lph = get_fuel_estimation(vehicle_data["readings"]["Speed"])		#Get Fuel consumption in lph
        	vehicle_data["readings"]["FuelConsumption"] = lph
	        fuel_consumed = lph * (now - prev_time) / 3600
        	fuel_level = fuel_level - fuel_consumed        

	        vehicle_data["GPS"] = {}
        	vehicle_data["GPS"]["coordinates"] = [gps_data.fix.longitude,gps_data.fix.latitude]
	        #vehicle_data["GPS"]["SignalStrength"] = gps_data.satellites
        	#vehicle_data["GPS"]["Heading"] = gps_data.fix.heading

	        #	print(json.dumps(vehicle_data))

        	status_code = send_data_to_vi(vehicle_data)

        	# Set now time as previous time.
        	prev_time = time.time()
        	
	        print_text("Data Posted at " + str(time.time()) + " Status Code:"  + str(status_code))

        	time.sleep(2)

except(KeyboardInterrupt, SystemExit):

#	Send Fuel Level in end.
	send_fuel_data_to_vi()

#	Update Fuel Level
	update_fuel_value(fuel_level)
	mysql_db.close_connection()

#	Send Ignition Status - ON
	send_ignition_status_to_vi("Off")

#   Stop Polling now
	gpsp.stop_polling()
	print_text(gpsp.get_polling_status())
	gpsp.join()

print_text("program complete")
