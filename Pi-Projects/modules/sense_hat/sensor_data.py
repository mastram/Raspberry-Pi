#import the sensor library
from sense_hat import SenseHat
from datetime import datetime
import time

def get_sense_data():

    sense = SenseHat()

    # Define list
    sense_data = []

    # Append sensor data
    sense_data.append(sense.get_temperature_from_humidity())
    sense_data.append(sense.get_temperature_from_pressure())
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())

    # Get orientation from sensor
    yaw,pitch,roll = sense.get_orientation().values()
    sense_data.extend([pitch,roll,yaw])

    # Get magnetic field (compass)
    mag_x,mag_y,mag_z = sense.get_compass_raw().values()
    sense_data.extend([mag_x,mag_y,mag_z])

    # Get accelerometer values
    x,y,z = sense.get_accelerometer_raw().values()
    sense_data.extend([x,y,z])

    # Get Gyro values
    gyro_x,gyro_y,gyro_z = sense.get_gyroscope_raw().values()
    sense_data.extend([gyro_x,gyro_y,gyro_z])

    # Add capture time
    sense_data.append(datetime.now())

    # Add precise time
    sense_data.append(int(round(time.time()*1000)))

    return sense_data
