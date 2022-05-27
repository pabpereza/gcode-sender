import RPi.GPIO as GPIO           # import RPi.GPIO module  
from time import sleep
import os
import requests
from service_controller import g_code_sender as sender


## PIN CONFIGURATION ##
## -------------------------------------------------- ##
GPIO.setmode(GPIO.BCM)          # choose BCM or BOARD  
# Pin control
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# Services status
# Auto in
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Lock out
GPIO.setup(6, GPIO.OUT)
# Seta
GPIO.setup(4, GPIO.IN , pull_up_down=GPIO.PUD_DOWN)

## PARSE BINARY POSITIONS ##
## -------------------------------------------------- ##
positions = []
with open('gpio_positions') as file:
    for line in file:
        positions.append(line.strip())


## AUXILAR FUNCTIONS ##
## -------------------------------------------------- ##
def finishProgram():
    os.system("curl -X GET http://localhost:8080/stop")
    #UNCOMMENTos.system("systemctl stop gpio-lector")
    exit(1)

def getPath(index_position):
    data = request.get("http://localhost:8080/position/" +str(index_position))
    path = data.get_json()["path"]
    return path

def translatePosition(bin_position):
    try:
        index = positions.index(bin_position) + 1
        return index
    except:
        print("La posicion introducida no esta en la lista")
        return False

def sendProgram(index_position):
    print("Enviando programa a puesto: " + str(position))
    sender.sendGCode( getPath(index_position) )

def programStatus():
    return False

def debug():
    if not GPIO.input(4):
        print("Se ha pulsado la seta")
    else:
        print("No se ha pulsado la seta")
    if not GPIO.input(5):
        print("Desactivado el modo auto")

## MAIN LOGIC PROCESS ##
## -------------------------------------------------- ##
try:
    while True:

        last_bin_position = "0000"

        # Comprobar si la seta esta pulsada o el pin auto estan activos
        if not GPIO.input(4) or not GPIO.input(5):
            debug()
            finishProgram()
        else:

            pin1 = GPIO.input(27)
            pin2 = GPIO.input(22)
            pin3 = GPIO.input(25)
            pin4 = GPIO.input(24)

            # Obteniendo pines de control y traduciendo a puesto 
            bin_position = str(pin1) + str(pin2) + str(pin3) + str(pin4) 
            
            print("Puesto en binario: " + bin_position)
            index_position = translatePosition(bin_position)

            if bin_position != "0000" and not index_position and bin_position != last_bin_position:
                    # Activar bloqueo de la inyectora
                    GPIO.output(6, True)
                    
                     # Enviar programa a puesto
                    sendProgram(index_position)
                    last_bin_position = bin_position 
                    GPIO.output(6, False)
                    sleep(2)


        sleep(2)
        print("---------------------------------------------")

finally:
    GPIO.cleanup()




