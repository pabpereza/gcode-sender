#!/usr/bin/python
"""\
Simple g-code streaming script
"""
import logging

from serial import Serial
import time
import sys

logging.basicConfig(filename='gcode_sender.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# TODO: Check if serial is connected
class GcodeSender:

    def __init__(self):
        self.serial = None

    def connect(self):
        try:
            self.serial = Serial('/dev/ttyACM0', 115200)
            logging.info("Serial connected")

        except Exception as e:
            logging.error("Serial error, " + str(e))
            raise e

    def remove_comment(self, string):
        if string.find(';') == -1:
            return string
        else:
            return string[:string.index(';')]

    def send_file(self, file_path):
        f = None
        try:
            logging.info("Reading file " + str(file_path))
            f = open(file_path, 'r')

            # Wake up
            logging.info("Wake up")
            # TODO: Check if necessary wakeup
            self.serial.write("\r\n\r\n")  # Hit enter a few times to wake
            time.sleep(2)  # Wait for Printrbot to initialize
            self.serial.flushInput()  # Flush startup text in serial input

            logging.info("Start - sending gcode")

            for line in f:
                l = self.remove_comment(line)
                l = l.strip()  # Strip all EOL characters for streaming
                if not l.isspace() and len(l) > 0:
                    logging.debug("Send:" + str(l))
                    l = l + '\n'
                    l_bytes = bytes(l, 'utf8')  # Adaptation of python2 to python3
                    self.serial.write(l_bytes)  # Send g-code block
                    grbl_out = self.serial.readline()  # Wait for response with carriage return
                    logging.debug("Response:" + str(grbl_out))

            logging.info("End - sending gcode")

        except Exception as e:
            logging.error("Error send file, " + str(e))
            raise e

        finally:
            try:
                f.close()
            except Exception as e:
                logging.error("Error close file, " + str(e))


# Command line purpose
if __name__ == "__main__":
    gcs = GcodeSender()
    path = sys.argv[1]
    gcs.send_file(path)
