
import time
import picamera


import zbarlight
import os
import sys
import PIL
import numpy as np

def get_image():
  with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    camera.capture('foo.jpg')
    





#print ('Taking picture..')
try:
    f = 1
    #qr_count = len(os.listdir('qr_codes'))
    get_image()
    #os.system('sudo fswebcam -d /dev/video'+sys.argv[1]+' -q qr_codes/qr_'+str(qr_count)+'.jpg')
    #print ('Picture taken..')
except Exception as e:
    f = 0
    #print ('Picture couldn\'t be taken with exception ' + str(e))

print

if(f):
    #print ('Scanning image..')
    f = open('foo.jpg','rb')
    qr = PIL.Image.open(f);
    qr.load()

    codes = zbarlight.scan_codes('qrcode',qr)
    if(codes==None):
        #os.remove('qr_codes/qr_'+str(qr_count)+'.jpg')
        print ("False")
    else:
        print (codes)
        
