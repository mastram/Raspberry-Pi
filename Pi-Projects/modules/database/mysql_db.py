############################
##   MySQL DB Functions   ##
############################

### Libraries ###
import MySQLdb
from ..config import mysql_config

### Logging Settings ###

### Global Variables ###

### Functions ###
def  open_connection() :
    global mysql_connection
    global mysql_cursor
    mysql_connection = MySQLdb.connect(mysql_config.db_host,mysql_config.db_user,mysql_config.db_pwd,mysql_config.db_name)
    mysql_cursor = mysql_connection.cursor()

def commit_data() :
    global mysql_connection
    mysql_connection.commit()

def close_connection() :
    global mysql_connection
    mysql_connection.commit()
    mysql_connection.close()

def get_cursor() :
    global mysql_cursor
    return mysql_cursor

def write_sensor_data_to_local_db(sensor_data) :

    global mysql_cursor
    
    # Form insert query
    insert_query = ("INSERT INTO sense_hat_data (temp_humidity, temp_pressure, pressure, humidity, pitch, roll, yaw, compass_x, compass_y, compass_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, capture_time, capture_timestamp, comment) "
                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                   
    mysql_cursor.execute(insert_query, sensor_data)
