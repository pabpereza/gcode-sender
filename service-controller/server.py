# Flask application for be the web panel of the server
import os
import controller
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def index():
	# Return status of the server
	return "OK"

@app.route('/start')
def start():
	# Start the server
	return controller.start()

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

@app.route('/positions', methods=['GET', 'POST'])
def positions():
	if request.method == 'POST':
		data = request.get_json()
		print(data)
		'''return controller.setPosition(request.json)'''
		return "OK"
	else:
		return controller.getPositions()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)