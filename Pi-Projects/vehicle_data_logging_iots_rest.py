########################################################

##   Vehicle Data Logging via REST Interface to IoT   ##

########################################################

from modules.gps_poller import gps_poller

from modules.config import vi
from modules.config import iots_config

from modules.database  import mysql_db



import time

import argparse

import json

import requests



### IoT Service Settings ###
iots_host = iots_config.iots_host
config_credentials_key= iots_config.config_credentials_key
config_credentials_crt= iots_config.config_credentials_crt
cap_veh_data = iots_config.cap_veh_data
sensor_id = iots_config.sensor_id
device_id = iots_config.device_id



### Logging Settings ###





### Global Settings ###



# GPS

gpsp = gps_poller.GpsPoller()

gpsp.start()



global send_data

# By default start sending

send_data = True



global prev_time

global fuel_level

global sleep_time

global min_gps_sat_count





### Argument Handling ###

parser = argparse.ArgumentParser()

parser.add_argument("-output",help="Print Results or not",type=int,default=0)

parser.add_argument("-comment",help="Comment",default="Test Logging")



args = parser.parse_args()



to_print = True

if args.output == 1 : to_print = True



comment = args.comment

fuel_level = 0;



def print_text(text) :

	if to_print : print(text)



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



def send_data_to_iots(post_data) :

    

    try:

    	headers = {'Content-type': 'application/json'}

    	url = iots_host + '/iot/gateway/rest/measures/' + device_id

    	r = requests.post(url, data=json.dumps(post_data), headers=headers, cert=(config_credentials_crt, config_credentials_key))

    	#print_text(url)

    	#print_text(json.dumps(post_data))

    	#print_text(config_credentials_crt)

    	#print_text(config_credentials_key)

    	return r.status_code

    

    except Exception as ex:

    	print_text(str(ex))

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



def send_location_data_to_vi() :

	gps_data = gpsp.get_current_value()

	lat = gps_data.fix.latitude

	lon = gps_data.fix.longitude

	speed = gps_data.fix.speed * 3.6



	vehicle_data = {}

	vehicle_data["capabilityAlternateId"] = cap_veh_data

	vehicle_data["sensorAlternateId"] = sensor_id

	geojson = {"type":"Point", "coordinates":[lon,lat]}

	# vehicle_data["measures"] = [{"Longitude":lon, "Latitude":lat, "GeoJson":json.dumps(geojson)}]

	vehicle_data["measures"] = [{"Longitude":lon, "Latitude":lat, "Speed":speed}]

	status_code = send_data_to_iots(vehicle_data)

	#print_text("Post data: " + json.dumps(vehicle_data))

	print_text("Location data Posted at " + str(time.time()) + " Status Code:" + str(status_code))



def send_ignition_status_to_vi(igni_status) :

	gps_data = gpsp.get_current_value()

	lat = gps_data.fix.latitude

	lon = gps_data.fix.longitude



	vehicle_data = {}

	vehicle_data["capabilityAlternateId"] = cap_veh_data

	vehicle_data["sensorAlternateId"] = sensor_id

	vehicle_data["measures"] = [{"Longitude":lon, "Latitude":lat, "IgnitionStatus":igni_status}]
	print_text("Ignition data: " + str(vehicle_data))

	status_code = send_data_to_iots(vehicle_data)

	print_text("Ignition Status Posted at " + str(time.time()) + " Status Code:" + str(status_code))



def send_fuel_data_to_vi() :

	gps_data = gpsp.get_current_value()

	lat = gps_data.fix.latitude

	lon = gps_data.fix.longitude



	vehicle_data = {}

	vehicle_data["capabilityAlternateId"] = cap_veh_data

	vehicle_data["sensorAlternateId"] = sensor_id

	vehicle_data["measures"] = [{"Longitude":lon, "Latitude":lat, "FuelLevel":fuel_level}]

	status_code = send_data_to_iots(vehicle_data)

	print_text("Fuel Data Posted at " + str(time.time()) + " Status Code:" + str(status_code))



# ========================================================================



# === main starts here ===================================================



sleep_time = 15



# Add delay of 5 seconds

time.sleep(5)



# Open MySQL Connection

mysql_db.open_connection()



# GPS

print_text(gpsp.get_polling_status())





# do 5 times to initialize

i = 0

while i<5:

    gpsp.get_current_value()

    i = i+1



print_text("Loop Start")

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



		if i % 20 == 0:

			update_fuel_value(fuel_level)

			send_fuel_data_to_vi()



		gps_data = gpsp.get_current_value()

		now = time.time()

		speed = gps_data.fix.speed * 3.6

		status_code = send_location_data_to_vi();



		#Get Fuel consumption in lph

		lph = get_fuel_estimation(speed)

		fuel_consumed = lph * (now - prev_time) / 3600

		fuel_level = fuel_level - fuel_consumed



# 		Set now time as previous time.

		prev_time = time.time()

		time.sleep(sleep_time)



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
