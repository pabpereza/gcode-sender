# Flask application for be the web panel of the server
import os
from service_controller import controller
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Sharing absolute path with the controller
# global_dir = os.path.dirname(__file__)
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
    return jsonify({'msg': controller.stop()})


@app.route('/restart')
def restart():
    # Restart the server
    return jsonify({'msg': controller.restart()})


@app.route('/status')
def status():
    # Return status of the server
    return jsonify({'msg': controller.status()})


@app.route('/getcodes/')
def getcode():
    return controller.getCodes()


@app.route('/sendcode/<int:puesto>')
def sendcode(puesto):
    # Send the code to the specified position
    return controller.sendGCode(puesto)


@app.route('/position/<int:puesto>', methods=['GET'])
def position(puesto):
    return jsonify(controller.getPosition(puesto))


@app.route('/positions', methods=['GET', 'POST'])
def positions():
    if request.method == 'POST':
        data = request.get_json()
        return controller.setPosition(int(data['position']))
    else:
        return controller.getPositions()


@app.route('/paths', methods=['GET'])
def paths():
    '''
    Get all paths
    '''
    return jsonify(controller.getPaths())


@app.route('/position/path', methods=['POST'])
def positionpath():
    '''
    Update position path
    '''
    # Get data
    data = request.get_json()
    position = int(data['position'])
    path = str(data['path'])

    # Update postion path
    msg = controller.updatePositionPath(position, path)

    # Return message (Ok , ERROR)
    return jsonify({'msg': msg})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
