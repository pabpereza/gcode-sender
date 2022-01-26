#  Function to control qr-lector service
import os


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