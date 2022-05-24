# Flask application for be the web panel of the server
import os
from service_controller import controller
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Sharing absolute path with the controller
global_dir = os.path.dirname(__file__)
global_dir = "/home/pi/qr-lector-and-gcode-sender" 

controller.setGlobalDir(global_dir)

@app.route('/')
def index():
	# Return status of the server
	return "OK"

@app.route('/seta')
def start():
	# Start the server
	return controller.seta()

@app.route('/stop')
def stop():
	# Stop the server
	return controller.stop()

@app.route('/restart')
def restart():
	# Restart the server
	return controller.restart()

@app.route('/status')
def status():
	# Return status of the server
	return controller.status()


@app.route('/getcodes/')
def getcode():
	return controller.getCodes()

@app.route('/sendcode/<int:puesto>')
def sendcode(puesto):
	# Send the code to the specified position
	return controller.sendGCode(puesto)

@app.route('/positions', methods=['GET', 'POST'])
def positions():
	if request.method == 'POST':
		data = request.get_json()
		return controller.setPosition( int(data['position']) )
	else:
		return controller.getPositions()

@app.route('/paths', methods=['GET'])
def paths():
	return controller.getPaths()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)