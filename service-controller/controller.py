#  Function to control qr-lector service
import os
import json

def start():
	print("Starting qr-lector service")
	os.system("systemctl start qr-lector")


def stop():
	print("Stopping qr-lector service")
	os.system("systemctl stop qr-lector")


def restart():
	print("Restarting qr-lector service")
	os.system("systemctl restart qr-lector")


def status():
	print("Status of qr-lector service")
	os.system("systemctl status qr-lector") 


def getPositions():
	with open('positions.json') as json_file:
		data = json.load(json_file)
		return json.dumps(data)


def setPosition( position):

	with open('positions.json','w') as json_file:
		data = json.load(json_file)
		if data[position-1]['active'] == True:
			data[position-1]['active'] = False
		else:
			data[position-1]['active'] = True
		
		json_file.write(data)

def sendGCode( puesto ):

	with open('positions.json') as json_file:
		data = json.load(json_file)
		if data[puesto-1]['active'] == True:
			print("Enviando GCode")
			os.system("python3 /home/pi/qr-lector/sendGCode.py " + str(data[puesto-1]['path']))
		else:
			print("Puesto no activo")
