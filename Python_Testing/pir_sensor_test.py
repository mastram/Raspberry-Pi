import RPi.GPIO as GPIO
from time import sleep

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(sensor, GPIO.IN)

print("PIR Test started")

previous_state = False
current_state = False

while True:
    print("Waiting")
        
    sleep(1)
    previous_state = current_state
    current_state = GPIO.input(sensor)

    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor,new_state))
