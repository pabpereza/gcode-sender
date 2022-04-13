import RPi.GPIO as GPIO           # import RPi.GPIO module  
from time import sleep

GPIO.setmode(GPIO.BCM)          # choose BCM or BOARD  

# Pin control
GPIO.setup(4, GPIO.OUT) 

GPIO.output(7, True)

sleep(1)


GPIO.output(7, False)

GPIO.cleanup()
