from gpiozero import LED, Button
from time import sleep

button = Button(2)
led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
