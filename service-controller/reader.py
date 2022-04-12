import RPi.GPIO as GPIO           # import RPi.GPIO module  
from time import sleep

GPIO.setmode(GPIO.BCM)          # choose BCM or BOARD  

# Pin control
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# Services status
GPIO.setup(5, GPIO.IN) 
GPIO.setup(6, GPIO.IN)

try:
    while True:
        if GPIO.input(27):
            print("Pin 27 activated - Bit 1")
        if GPIO.input(22):
            print("Pin 22 activated - Bit 2")
        if GPIO.input(23):
            print("Pin 23 activated - Bit 3")
        if GPIO.input(24):
            print("Pin 24 activated - Bit 4")
        if GPIO.input(25):
            print("Pin 25 activated - Bit 5")
        if GPIO.input(5):
            print("Pin 5 activated - Bit restart")
        if GPIO.input(6):
            print("Pin 6 activated - Bit stop")
        sleep(0.5)
finally:
    GPIO.cleanup()
