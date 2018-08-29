config_broker='1e4bcf9a-3f25-45c3-85e2-f3a486ad18f6.canary.cp.iot.sap'
config_alternate_id_device='Varun_Pi01'
config_alternate_id_capability_up01='c_up01_Varun_Pi'
config_alternate_id_capability_up02='c_up02_Varun_Pi'
config_alternate_id_sensor='Varun_Pi01'

import sys
import time
from sense_hat import SenseHat

# as an additional / non standard module pre-condition: 
# install Paho MQTT lib e.g. from https://github.com/eclipse/paho.mqtt.python
import paho.mqtt.client as mqtt

# Global Variables
sense = SenseHat()

# ========================================================================
def on_connect_broker(client, userdata, flags, rc):
	print('Connected to MQTT broker with result code: ' + str(rc))
	sys.stdout.flush()

def on_subscribe(client, obj, message_id, granted_qos):
	print('on_subscribe - message_id: ' + str(message_id) + ' / qos: ' + str(granted_qos))
	sys.stdout.flush()

def on_message(client, obj, msg):
	# print('on_message - ' + msg.topic + ' ' + str(msg.qos))
	print('on_message - ' + msg.topic + ' ' + str(msg.qos) + ' ' + str(msg.payload))
	sense.show_message("Hi Varun! MQTT Message Recieved",scroll_speed = 0.10)
	sys.stdout.flush()
# ========================================================================

# === main starts here ===================================================

config_crt_4_landscape='./eu10cpiotsap.crt'
config_credentials_key='./credentials.key'
config_credentials_crt='./credentials.crt'

broker=config_broker
broker_port=8883

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

print("connected to broker now")
sys.stdout.flush()

my_publish_topic='measures/' + my_device
my_subscription_topic='commands/' + my_device
client.subscribe(my_subscription_topic, 0)

client.loop_start()

sleep_time=10
time.sleep(sleep_time)

while True:
	print('in main loop')
	sys.stdout.flush()

	time.sleep(sleep_time)
	payload='{ "capabilityAlternateId" : "' + config_alternate_id_capability_up01 + '", "measures" : [[ "value for p01_up01", "value for p02_up01" ]], "sensorAlternateId":"' + config_alternate_id_sensor + '" }'
	result=client.publish(my_publish_topic, payload, qos=0)
	print("published for capability up01 with result: " + str(result))
	sys.stdout.flush()

	time.sleep(sleep_time)
	payload='{ "capabilityAlternateId" : "' + config_alternate_id_capability_up02 + '", "deviceAlternateId":"Varun_Pi01", "deviceId":"10", ' + '"measures" : [[ "value for p01_up02", "value for p02_up02" ]], "sensorAlternateId":"' + config_alternate_id_sensor + '" }'
	result=client.publish(my_publish_topic, payload, qos=0)
	print("published for capability up02 with result: " + str(result))
	sys.stdout.flush()
