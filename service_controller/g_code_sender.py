#!/usr/bin/python
"""\
Simple g-code streaming script
""" 
import serial
import time
import argparse


def sendGCode( path):

    # show values ##
    # print ("USB Port: %s" % args.port )
    print ("Gcode file: %s" % path )

    # Open serial port
    #s = serial.Serial('/dev/ttyACM0',115200)
    s = serial.Serial('/dev/ttyACM0',115200)
    print('Opening Serial Port')
    
    # Open g-code file
    f = open(args.file,'r');
    #f = open(args.file,'r');
    print('Opening gcode file')
    
    # Wake up 
    s.write("\r\n\r\n") # Hit enter a few times to wake the Printrbot
    time.sleep(2)   # Wait for Printrbot to initialize
    s.flushInput()  # Flush startup text in serial input
    print('Sending gcode')
    
    # Stream g-code
    for line in f:
        l = removeComment(line)
        l = l.strip() # Strip all EOL characters for streaming
        if  (l.isspace()==False and len(l)>0) :
            print('Sending: ' + l)
            s.write(l + '\n') # Send g-code block
            grbl_out = s.readline() # Wait for response with carriage return
            print(' : ' + grbl_out.strip())
    

    # Close file and serial port
    f.close()
    s.close()



def removeComment(string):
    if (string.find(';')==-1):
        return string
    else:
        return string[:string.index(';')]