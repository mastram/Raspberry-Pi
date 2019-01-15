############################
##   Sensor Data Logging  ##
############################
from modules.sense_hat import sensor_data
from modules.database  import hana_db
import time
import argparse

import sys
import time
import json
import socket
import fcntl
import struct

from datetime import datetime

### MQTT Connection Details
config_broker='1e4bcf9a-3f25-45c3-85e2-f3a486ad18f6.canary.cp.iot.sap'
config_alternate_id_device='263a6aa40e2c703f'

cap_accelerometer_data = 'IG_CE2D0000DF97B86A16007E06A1A79B5A'
cap_weather_data = 'IG_D02D0000DF97B86A16007E06A1A79B5A'

config_alternate_id_sensor='78a7cd4a9d271e45'

# Import MQTT Client 
import paho.mqtt.client as mqtt

# ============== Function List Starts Here ==========================

## Send data to PdMS
def send_data_to_pdms():

	sensor_readings = sensor_data.getSenseHatData()

	## Publish Accelerometer Data
	# Get accelerometer values
    x,y,z = sensor_readings.get_accelerometer_raw().values()

	measures = {}
	measures["I_ForceX"] = x
	measures["I_ForceY"] = y
	measures["I_ForceZ"] = z

	payload = {}
	payload["capabilityAlternateId"] = cap_accelerometer_data
	payload["sensorAlternateId"] = config_alternate_id_sensor
	payload["measures"] = measures
	
	result=client.publish(my_publish_topic, json.dumps(payload), qos=0)


	## Publish Weather Data
	# Get accelerometer values
    x,y,z = sensor_readings.get_accelerometer_raw().values()

	measures = {}
	measures["I_Temperature"] = sensor_readings.get_temperature_from_humidity()
	measures["I_Pressure"] = sensor_readings.get_pressure()

	payload = {}
	payload["capabilityAlternateId"] = cap_weather_data
	payload["sensorAlternateId"] = config_alternate_id_sensor
	payload["measures"] = measures
	
	result=client.publish(my_publish_topic, json.dumps(payload), qos=0)

# ============== Function List End Here    ==========================


# === main starts here ===================================================

### Logging Settings ###
# Commit after how many rows?
commit_frequency = 50

### Argument Handling ###
parser = argparse.ArgumentParser()
parser.add_argument("-ttl",help="Time to log",type=int,default=15)
parser.add_argument("-comment",help="Comment",default="Test Logging")

args = parser.parse_args()

time_to_log = args.ttl
comment = args.comment

# Keys
config_crt_4_landscape='/home/pi/Pi-Projects/eu10cpiotsap.crt'
config_credentials_key='/home/pi/Pi-Projects/credentials.key'
config_credentials_crt='/home/pi/Pi-Projects/credentials.crt'

broker=config_broker
broker_port=8883

## Connect to MQTT Client
my_device=config_alternate_id_device
client=mqtt.Client(client_id=my_device)
client.on_connect=on_connect_broker
client.on_subscribe=on_subscribe
client.on_message=on_message

client.tls_set(config_crt_4_landscape, certfile=config_credentials_crt, keyfile=config_credentials_key)

not_connected=True
while not_connected:
# {
	try:
		client.connect(broker, broker_port, 60)
		not_connected=False
	except:
		print("not connected yet")
		sys.stdout.flush()
		time.sleep(5)
# } while

print('+++++++++++++++++++++++++++++++++++++++++++++++++')
print("connected to broker now")
sys.stdout.flush()

## Subscribe to topics and publish
my_publish_topic='measures/' + my_device
my_subscription_topic='commands/' + my_device
client.subscribe(my_subscription_topic, 0)

# do 5 times to initialize
i = 0
while i<5:
    sensor_readings = sensor_data.get_sense_data()
    i = i+1

# Reset counter
i = 0

print("loop start")
start_time = time.time()
now = time.time()

while now < start_time + time_to_log:

	send_data_to_pdms()
    now = time.time()

    # Sleep for 3 seconds and send again.
    time.sleep(3)


print("program complete")