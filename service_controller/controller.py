#  Function to control gpio-lector service
import os
import json
import logging
from time import sleep
import glob

global_dir = '/home/pi/qr-lector-and-gcode-sender'
locked = False
service_name = "gpio-lector"

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def lockInterface():
    locked = True
    return 'locked'

def unlockInterface():
    locked = False
    return 'unlocked'


def setGlobalDir(direction):
    global global_dir
    global_dir = direction


def seta():
    print("Pulsada la seta")
    sendGCode(0)


def stop():
    print("Stopping " + service_name + "service")
    os.system("systemctl stop gpio-lector")
    sleep(2)
    return status()


def restart():
    print("Restarting " + service_name + " service")
    os.system("systemctl restart " + service_name)
    sleep(3)
    return status()


def status():
    print("Status of " + service_name + " service")
    status = os.system("systemctl is-active " + service_name)
    if str(status).strip() == "active":
        return True
    else:
        error_log = os.system("systemctl status " + service_name)
        logging.error(error_log)
        return False


def getPosition(position):
    with open(global_dir + '/service_controller/positions.json') as json_file:
        data = json.load(json_file)
        pos = {}

        for d in data:
            if d['position'] == int(position):
                pos = d
        return pos


def getPositions():
    with open(global_dir + '/service_controller/positions.json') as json_file:
        data = json.load(json_file)
        return json.dumps(data)


def setPosition(position):

    if not locked:

        json_file = open(global_dir + '/service_controller/positions.json')
        data = json.load(json_file)
        json_file.close()

        data[position - 1]['active'] = not data[position - 1]['active']

        if not data == "":
            json_file = open(global_dir + '/service_controller/positions.json', 'w')
            json.dump(data, json_file)
            json_file.close()
            return "OK"

        return "ERROR"


def updatePositionPath(position, path):
    json_file = open(global_dir + '/service_controller/positions.json')
    data = json.load(json_file)
    json_file.close()

    data[position - 1]['path'] = path

    if not data == "":
        json_file = open(global_dir + '/service_controller/positions.json', 'w')
        json.dump(data, json_file)
        json_file.close()
        return "OK"

    return "ERROR"


def getPaths():
    '''
    Get all paths from paths.json
    '''
    # TODO: modify ./ , use global_dir
    base = global_dir + '/service_controller/'
    files = glob.glob(base + 'robot_files/**/*.py', recursive=True)
    files = list(map(lambda x: x.replace(base, ''), files))
    return files


def getCodes():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(global_dir + '/service_controller/robot_files'):
        print(dirnames, filenames)

    return "OK"



## AUXILIAR FUNCTIONS ##
## ------------------ ##
def searchPath(puesto):
    with open(global_dir + '/service_controller/positions.json') as json_file:
        data = json.load(json_file)
        return data[puesto - 1]['path']


def checkIfPositionIsActive(puesto):
    with open(global_dir + '/service_controller/positions.json') as json_file:
        data = json.load(json_file)
        return data[puesto - 1]['active']
