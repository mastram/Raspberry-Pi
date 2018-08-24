#import the sensor library
#from common.sensor_data import get_sense_data
from common import sensor_data
from sense_hat import SenseHat

#sense.show_message("Read sensor data")

print ("Read sensor data")

sense = SenseHat()
t = sense.get_temperature()
p = sense.get_pressure()
h = sense.get_humidity()

t = round(t,3)
p = round(p,3)
h = round(h,3)

msg = "Temp is %s, Pres is %s, Humidity is %s" %(t,p,h)
print(msg)
#sense.show_message(msg,scroll_speed = 0.05)

#x,y,z = sense.get_accelerometer_raw().values()
x,y,z = sense.get_accelerometer().values()

x=round(x,3)
y=round(y,3)
z=round(z,3)

msg = "X is %s, Y is %s, Z is %s" %(x,y,z)
print(msg)
#sense.show_message(msg,scroll_speed = 0.05)

#gyro_x,gyro_y,gyro_z = sense.get_gyroscope_raw().values()
gyro_x,gyro_y,gyro_z = sense.get_gyroscope().values()

msg = "Gyro X is %s, Gyro Y is %s, Gyro Z is %s" %(gyro_x,gyro_y,gyro_z)
print(msg)

print("Read from module")
#sensor_readings = get_sense_data()
sensor_readings = sensor_data.get_sense_data()
#print(sensor_readings)
