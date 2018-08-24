############################
##   MySQL DB Functions   ##
############################

### Libraries ###
import pyhdb
from config import hana_config

### Logging Settings ###

### Global Variables ###

### Functions ###
def open_connection() :
    global hana_connection
    global hana_cursor

    hana_connection = pyhdb.connect(
        host = hana_config.db_host,
        port = hana_config.db_port,
        user = hana_config.db_user,
        password = hana_config.db_pwd
        )

    hana_cursor = hana_connection.cursor()

def commit_data() :
    global hana_connection
    hana_connection.commit()

def close_connection() :
    global hana_connection
    hana_connection.commit()
    hana_connection.close()
    
def write_sensor_data_to_hana_db(sensor_data) :

    # Remove the time in milli second
    length = len(sensor_data)
    del sensor_data[length - 2]
    
    global hana_cursor
    
    # Form insert query
    insert_query = ("INSERT INTO VERMAVA.sense_hat_data (temp_humidity, temp_pressure, pressure, humidity, pitch, roll, yaw, compass_x, compass_y, compass_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, capture_time, comments) "
                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                   
    hana_cursor.execute(insert_query, sensor_data)
