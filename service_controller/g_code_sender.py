#!/usr/bin/python
"""\
Simple g-code streaming script
"""
import logging

from serial import Serial
import time
import argparse
import sys

logging.basicConfig(filename='service.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def sendGCode(path):
    # show values ##
    # print ("USB Port: %s" % args.port )
    print("Gcode file: %s" % path)

    # Open serial port
    # s = serial.Serial('/dev/ttyACM0',115200)
    s = ""

    try:
        s = Serial('/dev/ttyACM0', 115200)
        print('Opening Serial Port')
    except:
        return "Encoladora no conectada \n"

    try:
        # Open g-code file
        f = open(path, 'r')
        # f = open(args.file,'r');
        logging.info("Reading file " + str(path))

        # Wake up 
        s.write("\r\n\r\n")  # Hit enter a few times to wake the Printrbot
        time.sleep(2)  # Wait for Printrbot to initialize
        s.flushInput()  # Flush startup text in serial input

        logging.info("Start - sending gcode")
        # Stream g-code
        for line in f:
            l = removeComment(line)
            l = l.strip()  # Strip all EOL characters for streaming
            if (l.isspace() == False and len(l) > 0):
                print('Sending: ' + l)
                s.write(l + '\n')  # Send g-code block
                grbl_out = s.readline()  # Wait for response with carriage return
                print(' : ' + str(grbl_out).strip())

        logging.info("End - sending gcode")
        # Close file and serial port
        f.close()
        s.close()
    except:
        logging.error("Error gcode " + str(path))
        return "Error en el puerto serie"

    return "OK"


def removeComment(string):
    if (string.find(';') == -1):
        return string
    else:
        return string[:string.index(';')]

if __name__ == "__main__":

    sendGCode(sys.argv[1])