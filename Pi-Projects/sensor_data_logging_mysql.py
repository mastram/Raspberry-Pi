############################
##   Sensor Data Logging  ##
############################
from modules.sense_hat import sensor_data
from modules.database  import mysql_db
import time
import argparse

### Logging Settings ###
# Commit after how many rows?
commit_frequency = 50

### Argument Handling ###
parser = argparse.ArgumentParser()
parser.add_argument("-ttl",help="Time to log",type=int,default=5)
parser.add_argument("-comment",help="Comment",default="Test Logging")

args = parser.parse_args()

time_to_log = args.ttl
comment = args.comment

## Main Program ##

# Open MySQL Connection
mysql_db.open_connection()

# do 5 times to initialize
i = 0
while i<5:
    sensor_readings = sensor_data.get_sense_data()
    i = i+1

print("loop start")
i=0
start_time = time.time()
now = time.time()

while now < start_time + time_to_log:

    sensor_readings = sensor_data.get_sense_data()
    sensor_readings.append(comment)

    mysql_db.write_sensor_data_to_local_db(sensor_readings)

    now = time.time()

    i=i+1
    if i%commit_frequency == 0:
        mysql_db.commit_data()

# Commit and Close connection
mysql_db.close_connection()

print("program complete")
