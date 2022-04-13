import RPi.GPIO as GPIO           # import RPi.GPIO module  
from time import sleep


## PIN CONFIGURATION ##
## -------------------------------------------------- ##
GPIO.setmode(GPIO.BCM)          # choose BCM or BOARD  
# Pin control
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
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

def translatePosition(bin_position):
   index = positions.index(bin_position) + 1
   return index

def sendProgram(position):
    print("Enviando programa a puesto: " + str(position))
    os.system("curl -X GET http://localhost:8080/sendcode/" + str(position))

def programStatus():
    return False

## MAIN LOGIC PROCESS ##
## -------------------------------------------------- ##
try:
    while True:

        # Candado de programa en ejecucion
        running_process = False

        # Comprobar si la seta esta pulsada o el pin auto estan activos
        if GPIO.input(4) or GPIO.input(5):
            finishProgram()

        # Comprobar si hay un programa en funcionamiento
        if not running_process:
            
            pin1 = GPIO.input(27)
            pin2 = GPIO.input(22)
            pin3 = GPIO.input(23)
            pin4 = GPIO.input(24)
            pin5 = GPIO.input(25)

            # Obteniendo pines de control y traduciendo a puesto 
            bin_position = str(pin1) + str(pin2) + str(pin3) + str(pin4) + str(pin5)
            print("Puesto en binario: " + bin_position)
            index_position = translatePosition(bin_position)

            # Activar bloqueo de la inyectora
            GPIO.output(6, True)

            # Enviar programa a puesto
            sendProgram(index_position)

       # Comprobar si el programa ha finalizado y desbloquear la inyectora 
        elif programStatus():
            GPIO.output(6, False)
            running_process = False
            print("Programa terminado, esperando al siguiente")
        
        sleep(0.5)

finally:
    GPIO.cleanup()




