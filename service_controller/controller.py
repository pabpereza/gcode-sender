#  Function to control gpio-lector service
import os
import json
from service_controller import g_code_sender as sender
import glob
from flask import jsonify

global_dir = '.'

def setGlobalDir(direction):
	global global_dir
	global_dir = direction 


def seta():
	print("Pulsada la seta")
	sendGCode(0)


def stop():
	print("Stopping gpio-lector service")
	os.system("systemctl stop gpio-lector")


def restart():
	print("Restarting gpio-lector service")
	os.system("systemctl restart gpio-lector")


def status():
	print("Status of gpio-lector service")
	os.system("systemctl status gpio-lector") 


def getPositions():
	with open( global_dir + '/service_controller/positions.json') as json_file:
		data = json.load(json_file)
		return json.dumps(data)


def setPosition( position):
	data = ""
	json_file = open(global_dir+ '/service_controller/positions.json')
	data = json.load(json_file)
	json_file.close()

	data[position-1]['active'] != data[position-1]['active'] !
	
	if not data == "":
		json_file = open(global_dir+ '/service_controller/positions.json','w')
		json.dump(data, json_file)
		json_file.close()
		return "OK"

	return "ERROR"


def getPaths():
	'''
	Get all paths from paths.json
	'''
	# TODO: modify ./ , use global_dir
	files = glob.glob('./service_controller/gcodes/**/*.gcode', recursive=True)
	files = list(map(lambda x : x.replace('./service_controller/', ''), files))
	return jsonify(files)

def setPath(path):
	data = ""
	json_file = open(global_dir+ '/service_controller/positions.json')
	data = json.load(json_file)
	json_file.close()

	data[position-1]['path'] = False
	
	if not data == "":
		json_file = open(global_dir+ '/service_controller/positions.json','w')
		json.dump(data, json_file)
		json_file.close()
		return "OK"

	return "ERROR"


def getCodes():
	f = []
	for (dirpath, dirnames, filenames) in os.walk( global_dir + '/GCodes' ):
		print(  dirnames, filenames)

	return "OK"

def sendGCode( puesto ):

	if puesto == 0:
		print("Send reset program")
		return "RESET"
	elif checkIfPositionIsActive(puesto):
		path = searchPath(puesto)
		print("Send GCode from: " + path + " to position: " + str(puesto))
		return sender.sendGCode( path )

	return "El puesto seleccionado no esta activo\n"

## AUXILIAR FUNCTIONS ##
## -------------------- ##
def searchPath( puesto):
	with open(global_dir + '/service_controller/positions.json') as json_file:
		data = json.load(json_file)
		return data[puesto-1]['path']


def checkIfPositionIsActive(puesto):
	with open(global_dir + '/service_controller/positions.json') as json_file:
		data = json.load(json_file)
		return data[puesto-1]['active']

