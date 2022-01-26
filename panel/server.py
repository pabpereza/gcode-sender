# Flask application for be the web panel of the server
import os
from flask import Flask
import controller

app = Flask(__name__)

@app.route('/')
def index():
	# Return status of the server
	return controller.status()


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

